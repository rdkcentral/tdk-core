## TestCase ID
NATIVE_PLAYBACK_361

## TestCase Name
NPVS_PlaySeek_Forward_HEVC_MKV

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective

Test to verify forward seek operation on H.265 MKV stream via `gst_element_seek()` with GST_SEEK_FLAG_FLUSH flag to seek to a specified position during active playback. The test validates accurate seek positioning, proper pipeline state handling during seek, and seamless playback recovery after seek completion. Verify playback position reaches the target seek position within Â±1 second tolerance via `gst_element_query_position()`, validate frame rendering via westerossinkâ†’stats show rendered_frames increment after seek, and confirm no errors on GStreamer bus.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | MKV H.265 stream must be accessible via HTTP (`souphttpsrc`) or local file system (`filesrc`) with matroskademux element. Stream path: `TDK_Asset_Sunrise_HEVC_MKV.mkv` | Verify MKV stream is accessible and contains valid H.265 and AAC representations |
| 3 | Stream Variable Configuration | `video_src_url_hevc_mkv` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "TDK_Asset_Sunrise_HEVC_MKV.mkv"` | Verify `video_src_url_hevc_mkv` resolves to valid location with correct codec support |
| 4 | Seek Test Configuration | NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT (default: 10 seconds) and NATIVE_PLAYBACK_SEEK_POSITION (default: 20 seconds for forward seek target position) must be configured in device config for forward seek operation timing and target position | Verify seek timeout configured for forward seek duration and seek target position configured for forward seek operation |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, Wayland display is created successfully, logging initialized without errors |
| 2 | Configure Seek Test Application | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (playback duration for each seek operation), `NATIVE_PLAYBACK_SEEK_POSITION` (target position for forward seek, default 20 seconds); Retrieve stream URL from `video_src_url_hevc_mkv` variable; Construct seek operation string with `seek:timeout:position`; Execute `mediapipelinetests test_trickplay <URL> operations=<seek_string>` to prepare seek test | Verify mediapipelinetests initializes with MKV stream and seek operation parameters correctly configured |
| 3 | Construct H.265 MKV Pipeline and Initiate Playing State | Create `playbin` element via `gst_element_factory_make()`; Configure `uri` property to `video_src_url_hevc_mkv` via `g_object_set()`; Set `westerossink` as video sink (or `autoaudiosink` for audio-only) via `g_object_set()`; Trigger state transition to `GST_STATE_PLAYING` via `gst_element_set_state()` | Verify playbin reaches `GST_STATE_PLAYING`, MKV matroskademux active and parsing stream, first frame rendered via first-video-frame-callback signal (or first audio sample for audio-only), no `GST_MESSAGE_ERROR` on bus |
| 4 | Query Initial Stream Properties | Query `westerossinkâ†’video-height` and `westerossinkâ†’video-width` via `g_object_get()` to confirm stream resolution (skip for audio-only); Query 
-audio` property via `g_object_get(playbin, "n-audio", &n_audio, NULL)` to verify AAC stream present; Query playback duration via `gst_element_query_duration()`; Log all stream properties | Verify video dimensions valid; Verify n-audio >= 1 confirming AAC stream detected; Verify stream duration retrieved successfully |
| 5 | Execute Forward Seek Operation | During active playback, invoke `gst_element_seek()` with `NORMAL_PLAYBACK_RATE`, `GST_FORMAT_TIME`, `GST_SEEK_FLAG_FLUSH`, `GST_SEEK_TYPE_SET`, and target seek position via `gst_element_seek(playbin, 1.0, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seek_position_in_nanoseconds, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)`; Pipeline automatically flushes pending buffers and transitions to specified position; Wait for async state change to complete | Verify `gst_element_seek()` call succeeds, pipeline transitions to new position, no `GST_MESSAGE_ERROR` on bus during seek |
| 6 | Validate Seek Position Accuracy | Poll `gst_element_query_position()` at 100ms intervals immediately after seek completion (for minimum 2 seconds) to verify current position matches seek target within Â±1 second tolerance; Monitor position should not exceed 1 second difference from target seek position | Verify position reaches target within Â±1 second; Verify position does not overshoot or undershoot beyond tolerance |
| 7 | Monitor Frame Rendering After Seek | Query westerossinkâ†’stats at 1-second intervals to verify `rendered_frames` counter increases after seek (pipeline recovers and resumes rendering); Verify `dropped_frames` < 1% of rendered_frames after seek operation; Confirm frame statistics show seamless recovery from seek state | Verify westerossinkâ†’stats to verify rendered_frames and dropped_frames show activity after seek, frame rendering resumes without extended stalls, dropped frame rate acceptable |
| 8 | Monitor GStreamer Bus for Errors | Monitor GStreamer message bus via `gst_bus_pop_filtered()` for `GST_MESSAGE_ERROR`, `GST_MESSAGE_WARNING`, or `GST_MESSAGE_EOS` messages during and after seek operations; Continue playback for full duration per timeout configuration; Log any error messages for analysis | Verify no errors detected on GStreamer bus during seek operation, playback continues normally after seek to completion |
| 9 | Monitor Playback Completion and Release Resources | If EOS received, verify test framework detects end-of-stream; Call `terminatePipeline(playbin)` to set state to `GST_STATE_NULL` via `gst_element_set_state()` and release all GStreamer objects (playbin, demuxer, westerossink, audioSink); Verify test output contains "Failures: 0" and "Errors: 0" or "failed: 0" confirming seek test passed | Verify clean pipeline shutdown reaching `GST_STATE_NULL`, all resources properly released, test output shows successful completion with 0 failures for forward seek operation |## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
