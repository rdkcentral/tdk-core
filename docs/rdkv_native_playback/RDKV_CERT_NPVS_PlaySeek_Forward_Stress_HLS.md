## TestCase ID
RDKV_NATIVE_PLAYBACK_68

## TestCase Name
RDKV_CERT_NPVS_PlaySeek_Forward_Stress_HLS

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify forward seek operations on H.264 HLS stream repeated in stress cycles. The test executes 3+ seek operations at different positions (incremented in fixed steps) to validate seek accuracy, position recovery, and playback continuity under stress conditions. Verify playback position matches seek target within +/-1 second tolerance after each seek operation, validate frame rendering resumes correctly via westerossink stats (rendered_frames increment), and detect no GStreamer errors during all seek cycles.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration |  HLS H.264 stream must be accessible via HTTP (`souphttpsrc`))<br>or local file system (`filesrc`))<br>with hlsdemux element. Stream path: `HLS_H264_AAC/master.m3u8` `video_src_url_hls` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "HLS_H264_AAC/master.m3u8"`  | Verify HLS stream is accessible and contains valid H.264 and AAC representations Verify `video_src_url_hls` resolves to valid location with correct codec support |
| 3 | Seek Test Configuration |  NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT (default: 10 seconds),<br>NATIVE_PLAYBACK_SEEK_POSITION (default: 20 seconds),<br>and NATIVE_PLAYBACK_SEEK_STEP (seek increment step for stress cycles))<br>must be configured in device config for forward seek operation timing and target position  | Verify seek timeout configured for forward seek duration and seek target position configured for forward seek operation |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment |  Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session<br>via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace  | Verify all environment variables load correctly, Wayland display is created successfully, logging initialized without errors |
| 2 | Configure Seek Test Application | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (playback duration for each seek operation), `NATIVE_PLAYBACK_SEEK_POSITION` (target position for forward seek, default 20 seconds);<br>Retrieve stream URL from `video_src_url_hls` variable;<br>Construct seek operation string with `seek:timeout:position` or multiple seek:position pairs for stress testing;<br>Execute `mediapipelinetests test_trickplay <URL> operations=<seek_string>` to prepare seek test | Verify mediapipelinetests initializes with HLS stream and seek operation parameters correctly configured |
| 3 | Construct H.264 HLS Pipeline and Initiate Playing State | Create `playbin` element via `gst_element_factory_make()`; Configure `uri` property to `video_src_url_hls` via `g_object_set()`;<br>Set `westerossink` as video sink (or `autoaudiosink` for audio-only) via `g_object_set()`;<br>Trigger state transition to `GST_STATE_PLAYING` via `gst_element_set_state()` | Verify playbin reaches `GST_STATE_PLAYING`, HLS hlsdemux active and parsing stream, first frame rendered via first-video-frame-callback signal (or first audio sample for audio-only), no `GST_MESSAGE_ERROR` on bus |
| 4 | Query Initial Stream Properties | Query `g_object_get(westerossink, "video-height")` and `g_object_get(westerossink, "video-width")` via `g_object_get()` to confirm stream resolution (skip for audio-only);<br>Query `g_object_get(playbin, "n-audio")` property via `g_object_get(playbin, "n-audio", &n_audio, NULL)` to verify AAC stream present;<br>Query playback duration via `gst_element_query_duration()`; Log all stream properties | Verify video dimensions valid; Verify n-audio >= 1 confirming AAC stream detected; Verify stream duration retrieved successfully |
| 5 | Execute Forward Seek Operation (repeated 3+ times per seek step) | During active playback, invoke `gst_element_seek()` with `NORMAL_PLAYBACK_RATE`, `GST_FORMAT_TIME`, `GST_SEEK_FLAG_FLUSH`, `GST_SEEK_TYPE_SET`, and target seek position via `gst_element_seek(playbin, 1.0, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seek_position_in_nanoseconds, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)`;<br>Pipeline automatically flushes pending buffers and transitions to specified position; Wait for async state change to complete | Verify `gst_element_seek()` call succeeds, pipeline transitions to new position, no `GST_MESSAGE_ERROR` on bus during seek |
| 6 | Validate Seek Position Accuracy | Poll `gst_element_query_position()` at 100ms intervals immediately after seek completion (for minimum 2 seconds) to verify current position matches seek target within +/-1 second tolerance;<br>Monitor position should not exceed 1 second difference from target seek position | Verify position reaches target within +/-1 second; Verify position does not overshoot or undershoot beyond tolerance |
| 7 | Monitor Frame Rendering After Seek | Query g_object_get(westerossink, "stats") at 1-second intervals to verify `rendered_frames` counter increases after seek (pipeline recovers and resumes rendering);<br>Verify `dropped_frames` < 1% of rendered_frames after seek operation; Confirm frame statistics show seamless recovery from seek state | Verify g_object_get(westerossink, "stats") to verify rendered_frames and dropped_frames show activity after seek, frame rendering resumes without extended stalls, dropped frame rate acceptable |
| 8 | Monitor GStreamer Bus for Errors | Monitor GStreamer message bus via `gst_bus_pop_filtered()` for `GST_MESSAGE_ERROR`, `GST_MESSAGE_WARNING`, or `GST_MESSAGE_EOS` messages during and after seek operations;<br>Continue playback for full duration per timeout configuration; Log any error messages for analysis | Verify no errors detected on GStreamer bus during seek operation, playback continues normally after seek to completion |
| 9 | Monitor Playback Completion and Release Resources | If EOS received, verify test framework detects end-of-stream;<br>Call `terminatePipeline(playbin)` to set state to `GST_STATE_NULL` via `gst_element_set_state()` and release all GStreamer objects (playbin, demuxer, westerossink, audioSink);<br>Verify test output contains "Failures: 0" and "Errors: 0" or "failed: 0" confirming seek test passed | Verify clean pipeline shutdown reaching `GST_STATE_NULL`, all resources properly released, test output shows successful completion with 0 failures for forward seek operation (repeated 3+ times per seek step) |## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121








