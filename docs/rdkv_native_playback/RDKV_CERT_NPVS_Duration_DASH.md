## TestCase ID
RDKV_NATIVE_PLAYBACK_192

## TestCase Name
RDKV_CERT_NPVS_Duration_DASH

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Query and validate H.264/AAC DASH stream duration using with parameter on playbin element. Verify DASH format manifest parsing correctly derives stream duration from MPD attribute and playbin duration query returns valid nanosecond value (not -1). Measure playback position advancement polling at 100ms intervals to confirm video renders correctly and duration accuracy matches expected 9-second baseline within GStreamer frame-sync tolerance.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation |  TDK_Package must be installed on the Device Under Test (DUT))<br>with `tdk_mediapipelinetests` binary and all dependent libraries including GStreamer 1.16+ with dashdemux, westerossink, and playbin elements  | Verify TDK_Package is installed, binary is executable, all libraries are available, and GStreamer plugins are loaded |
| 2 | Stream Provisioning and Configuration |  H.264/AAC video stream in DASH format must be accessible via HTTP/HTTPS or filesrc. Stream file path configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` in MediaValidationVariables.py (MPD manifest with 9+ second duration, H.264/AVC video codec, AAC audio codec in fMP4 segments))<br>Stream variable `video_src_url_dash` configured in `MediaValidationVariables.py` with path: `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` (DASH format with H.264 video, AAC audio, fMP4 segments)  | Verify MPD manifest is accessible via HTTPS or local filesystem, `dashdemux` can parse manifest without errors, mediaPresentationDuration attribute is present Verify `video_src_url_dash` resolves to valid, accessible MPD manifest location and manifest file size > 0 bytes |
| 3 | Playback Timeout Configuration |  Playback timeout `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds))<br>in device configuration file. Duration verification baseline set to 9 seconds for test comparison  | Verify timeout is set appropriately in configuration, duration baseline is 9 seconds |
| 4 | Platform-Specific Environment Variables |  Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor H.264 decoder libraries, `GST_PLUGIN_PATH`))<br>must be defined in `/opt/TDK/TDK.env` for H.264 hardware decoding support  | Verify `/opt/TDK/TDK.env` exists with all required environment variables, H.264 decoder plugins loaded via GST_PLUGIN_PATH |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment |  Source environment variables from `/opt/TDK/TDK.env` to load GStreamer H.264 decoder plugins, H.264 hardware library paths (`LD_PRELOAD` for vendor libraries),<br>and Wayland display configuration. Establish Wayland display session<br>via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace. Initialize audio FPS validation as enabled for DASH playback<br>via `checkAudioFPS=yes` argument  | Verify environment variables load correctly, H.264 decoder plugins available, Wayland display created successfully, logging initialized without errors |
|  2  |  Retrieve Configuration and Construct Playbin Pipeline  |   Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` from device configuration file (default 10 seconds). Retrieve stream variable `video_src_url_dash` from MediaValidationVariables.py. Create `playbin` element<br>via `gst_element_factory_make("playbin", NULL)`. Set URI property<br>via `g_object_set(playbin, "uri", <stream_url>, NULL)` with DASH MPD URL. Set playback flags to `GST_PLAY_FLAG_VIDEO  | GST_PLAY_FLAG_AUDIO` via `g_object_set(playbin, "flags", flags, NULL)`; GST_PLAY_FLAG_AUDIO` via `g_object_set(playbin, "flags", flags, NULL)`; Verify playbin element created successfully, stream URL configured without errors, flags set for A/V playback |
| 3 | Configure Westerossink and Register Callbacks |  Create `westerossink` element<br>via `gst_element_factory_make("westerossink", NULL)`. Connect as video sink to playbin<br>via `g_object_set(playbin, "video-sink", westerossink, NULL)`. Register `first-video-frame-callback` signal<br>via `g_signal_connect(westerossink, "first-video-frame-callback", G_CALLBACK(firstFrameCallback), &firstFrameReceived)` to detect when H.264 frame rendering begins  | Verify westerossink created successfully, connected as video sink, first-frame callback registered without errors |
| 4 | Transition Pipeline to PLAYING State | Set pipeline state to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)`<br> Poll `gst_element_get_state()` until state change completes (`GST_STATE_CHANGE_SUCCESS`)<br> Confirm `firstFrameReceived == true` callback was triggered indicating first H.264 frame rendered on sink | Verify pipeline reaches `GST_STATE_PLAYING` without `GST_MESSAGE_ERROR`, state transition completes synchronously or asynchronously, first-frame signal received |
| 5 | Query Stream Duration Using GStreamer Query API | Invoke `gst_element_query_duration(playbin, GST_FORMAT_TIME, &duration)` to retrieve total DASH stream duration in nanoseconds<br> Validate query returns TRUE (success)<br> Verify retrieved duration != -1 (indicates valid, parseable manifest)<br> For DASH streams, `dashdemux` derives duration from MPD `mediaPresentationDuration` attribute<br> Convert duration from nanoseconds to seconds via `GST_TIME_AS_SECONDS(duration)` and milliseconds via `GST_TIME_AS_MSECONDS(duration) % 1000` for logging and comparison | Verify duration query succeeds, returned value is positive integer (not -1), duration formatted correctly in M:SS.MS format |
| 6 | Validate Duration Matches Expected Baseline | Compare queried duration in seconds against expected baseline of 9 seconds<br> Calculate tolerance as +/-250 milliseconds (GStreamer seek granularity)<br> If queried duration falls within 8.75-9.25 second range, mark duration validation as PASS | Verify duration matches expected 9-second baseline within 250ms tolerance, duration mismatch logged for failure diagnosis |
| 7 | Monitor Playback Position Advancement |  Poll `gst_element_query_position(playbin, GST_FORMAT_TIME, &currentPosition)` at 100ms intervals during playback. Query westerossink `stats` property<br>via `g_object_get(westerossink, "stats", &structure, NULL)`. Extract `rendered_frames` and `dropped_frames` counters<br>via `gst_structure_get_uint64()`. Verify rendered_frames increments each second (no stalls), dropped_frames remains at 0 or below acceptable threshold (< 1% of rendered). Track playback position reaches at least stream duration limit  | Verify position increments continuously without backward jumps, frame rendering statistics show healthy video playback, no stalls or frame drops |
| 8 | Validate Test Success and Parse Output | Monitor GStreamer bus via `gst_bus_timed_pop_filtered()` for `GST_MESSAGE_EOS` (End-of-Stream) or `GST_MESSAGE_ERROR` messages<br> Verify test framework `checkMediaPipelineTestStatus` output contains strings "Failures: 0" and "Errors: 0" or "failed: 0" indicating clean execution<br> Execute `DurationParse` custom test step to extract duration from mediapipelinetests output log and verify matches expected 9-second value | Verify no `GST_MESSAGE_ERROR` detected on bus, test status shows zero failures and errors, duration parse step extracts and matches expected value |
| 9 | Release Pipeline and Cleanup Resources |  Set pipeline state to `GST_STATE_NULL`<br>via `gst_element_set_state(playbin, GST_STATE_NULL)`. Unreference playbin and westerossink objects<br>via `gst_object_unref()`. Close logging file. Verify all GStreamer resources are freed and memory deallocated  | Verify pipeline reaches `GST_STATE_NULL` cleanly, all objects unreferenced, no resource leaks detected, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 5 mins

**Priority:** High

**Release Version:** M121











