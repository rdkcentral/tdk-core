## TestCase ID
NATIVE_PLAYBACK_192

## TestCase Name
NPVS_Duration_Test_DASH

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Query and validate H.264/AAC DASH stream duration using  with  parameter on playbin element. Verify DASH format manifest parsing via `dashdemux` correctly derives stream duration from MPD `mediaPresentationDuration` attribute and playbin duration query returns valid nanosecond value (not -1). Measure playback position advancement via  polling at 100ms intervals to confirm video renders correctly and duration accuracy matches expected 9-second baseline within GStreamer frame-sync tolerance.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries including GStreamer 1.16+ with dashdemux, westerossink, and playbin elements | Verify TDK_Package is installed, binary is executable, all libraries are available, and GStreamer plugins are loaded |
| 2 | H.264/AAC DASH Stream Provisioning | H.264/AAC video stream in DASH format must be accessible via HTTP/HTTPS or filesrc. Stream file path configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` in MediaValidationVariables.py (MPD manifest with 9+ second duration, H.264/AVC video codec, AAC audio codec in fMP4 segments) | Verify MPD manifest is accessible via HTTPS or local filesystem, `dashdemux` can parse manifest without errors, mediaPresentationDuration attribute is present |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_dash` configured in `MediaValidationVariables.py` with path: `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` (DASH format with H.264 video, AAC audio, fMP4 segments) | Verify `video_src_url_dash` resolves to valid, accessible MPD manifest location and manifest file size > 0 bytes |
| 4 | Playback Timeout Configuration | Playback timeout `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in device configuration file. Duration verification baseline set to 9 seconds for test comparison | Verify timeout is set appropriately in configuration, duration baseline is 9 seconds |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor H.264 decoder libraries, ) must be defined in `/opt/TDK/TDK.env` for H.264 hardware decoding support | Verify `/opt/TDK/TDK.env` exists with all required environment variables, H.264 decoder plugins loaded via GST_PLUGIN_PATH |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer H.264 decoder plugins, H.264 hardware library paths (`LD_PRELOAD` for vendor libraries), and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace. Initialize audio FPS validation as enabled for DASH playback via `checkAudioFPS=yes` argument | Verify environment variables load correctly, H.264 decoder plugins available, Wayland display created successfully, logging initialized without errors |
| 2 | Retrieve Configuration and Construct Playbin Pipeline | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` from device configuration file (default 10 seconds). Retrieve stream variable `video_src_url_dash` from MediaValidationVariables.py. Create `playbin` element via . Set URI property via  with DASH MPD URL. Set playback flags to  via  | Verify playbin element created successfully, stream URL configured without errors, flags set for A/V playback |
| 3 | Configure Westerossink and Register Callbacks | Create `westerossink` element via . Connect as video sink to playbin via . Register `first-video-frame-callback` signal via  to detect when H.264 frame rendering begins | Verify westerossink created successfully, connected as video sink, first-frame callback registered without errors |
| 4 | Transition Pipeline to PLAYING State | Set pipeline state to  via . Poll  until state change completes (). Confirm `firstFrameReceived == true` callback was triggered indicating first H.264 frame rendered on sink | Verify pipeline reaches  without , state transition completes synchronously or asynchronously, first-frame signal received |
| 5 | Query Stream Duration Using GStreamer Query API | Invoke  to retrieve total DASH stream duration in nanoseconds. Validate query returns TRUE (success). Verify retrieved duration != -1 (indicates valid, parseable manifest). For DASH streams, `dashdemux` derives duration from MPD `mediaPresentationDuration` attribute. Convert duration from nanoseconds to seconds via  and milliseconds via  for logging and comparison | Verify duration query succeeds, returned value is positive integer (not -1), duration formatted correctly in M:SS.MS format |
| 6 | Validate Duration Matches Expected Baseline | Compare queried duration in seconds against expected baseline of 9 seconds. Calculate tolerance as ±250 milliseconds (GStreamer seek granularity). If queried duration falls within 8.75-9.25 second range, mark duration validation as PASS | Verify duration matches expected 9-second baseline within 250ms tolerance, duration mismatch logged for failure diagnosis |
| 7 | Monitor Playback Position Advancement |  Query westerossink `stats` property via . Extract `rendered_frames` and `dropped_frames` counters via . Verify rendered_frames increments each second (no stalls), dropped_frames remains at 0 or below acceptable threshold (< 1% of rendered). Track playback position reaches at least stream duration limit | Verify position increments continuously without backward jumps, frame rendering statistics show healthy video playback, no stalls or frame drops |
| 8 | Validate Test Success and Parse Output | Monitor GStreamer bus via  for  (End-of-Stream) or  messages. Verify test framework `checkMediaPipelineTestStatus` output contains strings "Failures: 0" and "Errors: 0" or "failed: 0" indicating clean execution. Execute `DurationParse` custom test step to extract duration from mediapipelinetests output log and verify matches expected 9-second value | Verify no  detected on bus, test status shows zero failures and errors, duration parse step extracts and matches expected value |
| 9 |  Close logging file. Verify all GStreamer resources are freed and memory deallocated | Verify pipeline reaches  cleanly, all objects unreferenced, no resource leaks detected, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3-5 minutes

**Priority:** High

**Release Version:** M121
