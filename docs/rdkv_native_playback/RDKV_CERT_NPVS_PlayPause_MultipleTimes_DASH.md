## TestCase ID
RDKV_NATIVE_PLAYBACK_179

## TestCase Name
RDKV_CERT_NPVS_PlayPause_MultipleTimes_DASH

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify stress-tested play-pause operations on H.264 DASH stream. The test executes 3+ complete play-pause cycles by repeatedly alternating between PLAYING and PAUSED states to validate state machine stability, resource cleanup, and playback recovery under stress conditions. Verify playback position advances at 1x rate ( second) during play and remains constant ( movement) during pause, validate frame rendering statistics via g_object_get(westerossink, "stats") show rendered_frames increment only during play state, and detect no GStreamer errors or buffer starvation issues throughout all stress cycles.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration | DASH H.264 AAC stream must be accessible via HTTP (`souphttpsrc`) or local file system (`filesrc`) with dashdemux element<br> Stream path: `DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd` `video_src_url_dash` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` | Verify DASH stream is accessible and contains valid H.264 and AAC representations Verify `video_src_url_dash` resolves to valid location with correct codec support |
| 3 | Stress Test Configuration |  `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds))<br>and `NATIVE_PLAYBACK_STRESS_REPEAT_COUNT` (default: 3))<br>must be configured in device config for play-pause operation duration and cycle repetition  | Verify timeout configured for playback operations and stress repeat count configured for 3+ cycles |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment |  Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session<br>via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace  | Verify all environment variables load correctly, Wayland display is created successfully, logging initialized without errors |
| 2 | Configure Stress Test Application | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (timeout for each play/pause operation, default: 10 seconds) and `NATIVE_PLAYBACK_STRESS_REPEAT_COUNT` (number of play-pause cycles, default: 3);<br>Retrieve stream URL from `video_src_url_dash` variable; Construct operations string with `play:<timeout>,pause:<timeout>` repeated 3+ times;<br>Execute `mediapipelinetests test_trickplay <URL> operations=<operations_string>` to prepare stress test | Verify mediapipelinetests initializes with DASH stream and stress operation parameters (operations string, repeat count) correctly configured |
| 3 | Construct H.264 DASH Pipeline and Initiate Playing State | Create `playbin` element via `gst_element_factory_make()`; Configure `uri` property to `video_src_url_dash` via `g_object_set()`;<br>Set `westerossink` as video sink via `g_object_set()`; Configure `autoaudiosink` for AAC audio via `g_object_set()`;<br>Trigger state transition to `GST_STATE_PLAYING` via `gst_element_set_state()` | Verify playbin reaches `GST_STATE_PLAYING`, DASH dashdemux active and parsing stream, first frame rendered via first-video-frame-callback signal, no `GST_MESSAGE_ERROR` on bus |
| 4 | Query Initial Stream Properties | Query `g_object_get(westerossink, "video-height")` and `g_object_get(westerossink, "video-width")` via `g_object_get()` to confirm stream resolution;<br>Query `g_object_get(playbin, "n-audio")` property via `g_object_get(playbin, "n-audio", &n_audio, NULL)` to verify AAC stream present;<br>Query playback duration via `gst_element_query_duration()`; Log all stream properties | Verify video dimensions valid; Verify n-audio >= 1 confirming AAC stream detected; Verify stream duration retrieved successfully |
| 5 | Execute Play-Pause Stress Cycles | For each cycle iteration (repeated 3+ times): Execute PLAY operation by setting pipeline to `GST_STATE_PLAYING` via `gst_element_set_state()` and maintaining for NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT seconds;<br>Then execute PAUSE operation by setting pipeline to `GST_STATE_PAUSED` via `gst_element_set_state()` and maintaining for NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT seconds;<br>Repeat 3+ complete play-pause cycles | Verify all 3+ play-pause cycle transitions complete successfully without errors, timeouts, or resource exhaustion; Verify pipeline state changes properly reflect via `gst_element_get_state()` |
| 6 | Monitor Playback Position During Play State | During each PLAYING state interval, poll `gst_element_query_position()` at 100ms intervals to verify position advances at 1x rate ( second tolerance per timeout window);<br>Verify position never halts or exhibits backward jumps during play intervals | Verify position increments smoothly at consistent 1x playback rate throughout all PLAYING periods; Verify no position stalls or anomalies detected |
| 7 | Validate Position Halt During Pause State | During each PAUSED state interval, poll `gst_element_query_position()` at 100ms intervals for minimum 1 second to verify position remains constant ( movement);<br>Confirm position does not drift or change during pause intervals across all stress cycles | Verify position remains completely stationary during all PAUSED state periods with  tolerance; Verify no position drift detected despite multiple pause-resume cycles |
| 8 | Validate Frame Rendering Statistics Under Stress | Query `g_object_get(westerossink, "stats")` at 1-second intervals during all play-pause cycles to verify `rendered_frames` counter increments ONLY during PLAYING state and remains static during PAUSED state;<br>Verify `dropped_frames` < 1% of rendered_frames throughout all stress cycles; Monitor frame statistics correlate directly with state transitions | Verify frame statistics show rendered_frames increment during play and remain static during pause for all 3+ cycles; Verify dropped frame rate acceptable throughout stress test |
| 9 | Monitor GStreamer Bus and Release Resources | Monitor GStreamer message bus via `gst_bus_pop_filtered()` for `GST_MESSAGE_ERROR`, `GST_MESSAGE_WARNING`, or `GST_MESSAGE_EOS` messages during all cycles;<br>Call `terminatePipeline(playbin)` to set state to `GST_STATE_NULL` via `gst_element_set_state()` and release all GStreamer objects (playbin, demuxer, westerossink, audioSink);<br>Verify test output contains "Failures: 0" and "Errors: 0" or "failed: 0" confirming all stress cycles passed | Verify no errors detected on GStreamer bus throughout all stress cycles; Verify clean pipeline shutdown reaching `GST_STATE_NULL`; Verify test output shows successful completion with 0 failures for 3+ play-pause stress cycles |## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121











