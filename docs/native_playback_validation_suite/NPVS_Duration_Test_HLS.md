## TestCase ID
NATIVE_PLAYBACK_193

## TestCase Name
NPVS_Duration_Test_HLS

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Query and validate H.264/AAC HLS stream duration using `gst_element_query_duration()` with `GST_FORMAT_TIME` parameter on playbin element. Verify HLS format playlist parsing via `hlsdemux` correctly calculates stream duration from segment information and playbin duration query returns valid nanosecond value (not -1). Measure playback position advancement via `gst_element_query_position()` polling at 100ms intervals to confirm video renders correctly and duration accuracy matches expected 9-second baseline within GStreamer frame-sync tolerance.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries including GStreamer 1.16+ with hlsdemux, westerossink, and playbin elements | Verify TDK_Package is installed, binary is executable, all libraries are available, and GStreamer plugins are loaded |
| 2 | H.264/AAC HLS Stream Provisioning | H.264/AAC video stream in HLS format must be accessible via HTTP/HTTPS or filesrc. Stream file path configured as `test_streams_base_path + "HLS_H264_AAC/master.m3u8"` in MediaValidationVariables.py (M3U8 playlist with 9+ second duration, H.264/AVC video codec, AAC audio codec in MPEG-2 TS segments) | Verify M3U8 playlist is accessible via HTTPS or local filesystem, `hlsdemux` can parse playlist without errors, segment duration information is available |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_hls` configured in `MediaValidationVariables.py` with path: `test_streams_base_path + "HLS_H264_AAC/master.m3u8"` (HLS format with H.264 video, AAC audio, MPEG-2 TS segments) | Verify `video_src_url_hls` resolves to valid, accessible M3U8 playlist location and playlist file size > 0 bytes |
| 4 | Playback Timeout Configuration | Playback timeout `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in device configuration file. Duration verification baseline set to 9 seconds for test comparison | Verify timeout is set appropriately in configuration, duration baseline is 9 seconds |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor H.264 decoder libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` for H.264 hardware decoding support | Verify `/opt/TDK/TDK.env` exists with all required environment variables, H.264 decoder plugins loaded via GST_PLUGIN_PATH |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer H.264 decoder plugins, H.264 hardware library paths (`LD_PRELOAD` for vendor libraries), and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace. Initialize audio FPS validation as enabled for HLS playback via `checkAudioFPS=yes` argument | Verify environment variables load correctly, H.264 decoder plugins available, Wayland display created successfully, logging initialized without errors |
| 2 | Retrieve Configuration and Construct Playbin Pipeline | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` from device configuration file (default 10 seconds). Retrieve stream variable `video_src_url_hls` from MediaValidationVariables.py. Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Set URI property via `g_object_set(playbin, "uri", <stream_url>, NULL)` with HLS M3U8 URL. Set playback flags to `GST_PLAY_FLAG_VIDEO \| GST_PLAY_FLAG_AUDIO` via `g_object_set(playbin, "flags", flags, NULL)` | Verify playbin element created successfully, stream URL configured without errors, flags set for A/V playback |
| 3 | Configure Westerossink and Register Callbacks | Create `westerossink` element via `gst_element_factory_make("westerossink", NULL)`. Connect as video sink to playbin via `g_object_set(playbin, "video-sink", westerossink, NULL)`. Register `first-video-frame-callback` signal via `g_signal_connect(westerossink, "first-video-frame-callback", G_CALLBACK(firstFrameCallback), &firstFrameReceived)` to detect when H.264 frame rendering begins | Verify westerossink created successfully, connected as video sink, first-frame callback registered without errors |
| 4 | Transition Pipeline to PLAYING State | Set pipeline state to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)`. Poll `gst_element_get_state()` until state change completes (`GST_STATE_CHANGE_SUCCESS`). Confirm `firstFrameReceived == true` callback was triggered indicating first H.264 frame rendered on sink | Verify pipeline reaches `GST_STATE_PLAYING` without `GST_MESSAGE_ERROR`, state transition completes synchronously or asynchronously, first-frame signal received |
| 5 | Query Stream Duration Using GStreamer Query API | Invoke `gst_element_query_duration(playbin, GST_FORMAT_TIME, &duration)` to retrieve total HLS stream duration in nanoseconds. Validate query returns TRUE (success). Verify retrieved duration != -1 (indicates valid, parseable playlist). For HLS streams, `hlsdemux` calculates duration by summing segment durations from M3U8 playlist. Convert duration from nanoseconds to seconds via `GST_TIME_AS_SECONDS(duration)` and milliseconds via `GST_TIME_AS_MSECONDS(duration) % 1000` for logging and comparison | Verify duration query succeeds, returned value is positive integer (not -1), duration formatted correctly in M:SS.MS format |
| 6 | Validate Duration Matches Expected Baseline | Compare queried duration in seconds against expected baseline of 9 seconds. Calculate tolerance as Â±250 milliseconds (GStreamer seek granularity). If queried duration falls within 8.75-9.25 second range, mark duration validation as PASS | Verify duration matches expected 9-second baseline within 250ms tolerance, duration mismatch logged for failure diagnosis |
| 7 | Monitor Playback Position Advancement | Poll `gst_element_query_position(playbin, GST_FORMAT_TIME, &currentPosition)` at 100ms intervals during playback. Query westerossink `stats` property via `g_object_get(westerossink, "stats", &structure, NULL)`. Extract `rendered_frames` and `dropped_frames` counters via `gst_structure_get_uint64()`. Verify rendered_frames increments each second (no stalls), dropped_frames remains at 0 or below acceptable threshold (< 1% of rendered). Track playback position reaches at least stream duration limit | Verify position increments continuously without backward jumps, frame rendering statistics show healthy video playback, no stalls or frame drops |
| 8 | Validate Test Success and Parse Output | Monitor GStreamer bus via `gst_bus_timed_pop_filtered()` for `GST_MESSAGE_EOS` (End-of-Stream) or `GST_MESSAGE_ERROR` messages. Verify test framework `checkMediaPipelineTestStatus` output contains strings "Failures: 0" and "Errors: 0" or "failed: 0" indicating clean execution. Execute `DurationParse` custom test step to extract duration from mediapipelinetests output log and verify matches expected 9-second value | Verify no `GST_MESSAGE_ERROR` detected on bus, test status shows zero failures and errors, duration parse step extracts and matches expected value |
| 9 | Release Pipeline and Cleanup Resources | Set pipeline state to `GST_STATE_NULL` via `gst_element_set_state(playbin, GST_STATE_NULL)`. Unreference playbin and westerossink objects via `gst_object_unref()`. Close logging file. Verify all GStreamer resources are freed and memory deallocated | Verify pipeline reaches `GST_STATE_NULL` cleanly, all objects unreferenced, no resource leaks detected, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3-5 minutes

**Priority:** High

**Release Version:** M121
