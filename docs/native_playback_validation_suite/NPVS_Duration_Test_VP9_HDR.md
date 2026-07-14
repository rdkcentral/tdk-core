## TestCase ID
NATIVE_PLAYBACK_375

## TestCase Name
NPVS_Duration_Test_VP9_HDR

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test validates duration metadata accuracy for VP9 video content with HDR support. Verifies that duration query accurately reports media duration matching the 9-second baseline, confirming proper parsing and duration extraction for HDR-enabled VP9 streams.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | WebM container with VP9 HDR video must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file configured as `test_streams_base_path + "TDK_Asset_Sunrise_VP9_HDR.webm"` in MediaValidationVariables.py. Stream contains VP9 video with HDR in WebM container format (for VP9 HDR duration testing) | Verify WebM file is accessible and readable from configured path, matroskademux parser available for duration extraction from segment information |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_vp9_hdr` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "TDK_Asset_Sunrise_VP9_HDR.webm"` | Verify `video_src_url_vp9_hdr` resolves to valid WebM container file with HDR and duration metadata |
| 4 | Playback Timeout Configuration | Playback timeout `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in device configuration file. Duration verification baseline set to 9 seconds for test comparison | Verify timeout is set appropriately in configuration, duration baseline is 9 seconds |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer VP9 decoder plugins with HDR support, VP9 HDR hardware library paths (`LD_PRELOAD` for vendor libraries), WebM demuxer plugin, and Wayland display configuration with HDR mode enabled. Establish Wayland display session via RDKWindowManager or westeros compositor with HDR capabilities. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify environment variables load correctly, VP9 HDR decoder plugins available, Wayland display created with HDR support, logging initialized without errors |
| 2 | Retrieve Configuration and Construct Playbin Pipeline | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` from device configuration file (default 10 seconds). Retrieve stream variable `video_src_url_vp9_hdr` from MediaValidationVariables.py. Create `playbin` element via . Set URI property via  with VP9 HDR WebM file URL. Set playback flags to  via  | Verify playbin element created successfully, stream URL configured without errors, flags set for A/V playback |
| 3 | Configure Westerossink with HDR Mode and Register Callbacks | Create `westerossink` element via . Connect as video sink to playbin via . Enable HDR mode on westerossink via  to support VP9 HDR profiles (HDR10, HLG). Register `first-video-frame-callback` signal via  to detect when VP9 HDR frame rendering begins | Verify westerossink created successfully, HDR mode enabled, connected as video sink, first-frame callback registered without errors |
| 4 | Transition Pipeline to PLAYING State | Set pipeline state to  via . Poll  until state change completes (). Confirm `firstFrameReceived == true` callback was triggered indicating first VP9 HDR frame rendered on sink with HDR color space. `webmdemux` element parses WebM container and initializes VP9 HDR video stream | Verify pipeline reaches  without , state transition completes synchronously or asynchronously, first-frame signal received in HDR mode |
| 5 | Query Stream Duration Using GStreamer Query API | Invoke  to retrieve total VP9 HDR WebM stream duration in nanoseconds. Validate query returns TRUE (success). Verify retrieved duration != -1 (indicates valid, parseable WebM file). For WebM VP9 HDR streams, `webmdemux` reads duration from EBML segment. Convert duration from nanoseconds to seconds via  and milliseconds via  for logging and comparison | Verify duration query succeeds, returned value is positive integer (not -1), duration formatted correctly in M:SS.MS format |
| 6 | Validate Duration Matches Expected Baseline | Compare queried duration in seconds against expected baseline of 9 seconds. Calculate tolerance as ±250 milliseconds (GStreamer seek granularity). If queried duration falls within 8.75-9.25 second range, mark duration validation as PASS | Verify duration matches expected 9-second baseline within 250ms tolerance, duration mismatch logged for failure diagnosis |
| 7 | Monitor Playback Position Advancement |  Query westerossink `stats` property via . Extract `rendered_frames` and `dropped_frames` counters via . Verify rendered_frames increments each second (no stalls), dropped_frames remains at 0 or below acceptable threshold (< 1% of rendered). Track playback position reaches at least stream duration limit. Monitor HDR metadata transfer during playback | Verify position increments continuously without backward jumps, frame rendering statistics show healthy video playback with HDR color rendering, no stalls or frame drops, HDR metadata processed correctly |
| 8 | Validate Test Success and Parse Output | Monitor GStreamer bus via  for  (End-of-Stream) or  messages. Verify test framework `checkMediaPipelineTestStatus` output contains strings "Failures: 0" and "Errors: 0" or "failed: 0" indicating clean execution. Execute `DurationParse` custom test step to extract duration from mediapipelinetests output log and verify matches expected 9-second value | Verify no  detected on bus, test status shows zero failures and errors, duration parse step extracts and matches expected value, HDR processing completed without errors |
| 9 |  Close logging file. Verify all GStreamer resources are freed and memory deallocated | Verify pipeline reaches  cleanly, HDR mode disabled, all objects unreferenced, no resource leaks detected, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3-5 minutes

**Priority:** High

**Release Version:** M121
