## TestCase ID
NATIVE_PLAYBACK_215

## TestCase Name
NPVS_Duration_Test_MP3

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate MP3 audio stream playback and audio pad query. Test validates duration metadata accuracy for MP3 audio content. Verifies that duration query accurately reports audio duration matching the 9-second baseline, confirming proper MP3 frame header parsing and duration calculation for audio-only streams.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | MP3 audio stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file configured as `test_streams_base_path + "TDK_Asset_Sunrise_MP3.mp3"` in MediaValidationVariables.py. Stream contains PCM audio data in MP3 format (audio-only stream for duration validation testing) | Verify MP3 file is accessible and readable from configured path, MP3 audio decoder plugins available for parsing |  
| 3 | Stream Variable Configuration | Stream variable `audio_src_url_mp3` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "TDK_Asset_Sunrise_MP3.mp3"` | Verify `audio_src_url_mp3` resolves to valid MP3 audio file, file contains valid MP3 frame headers and audio data |
| 4 | Playback Timeout Configuration | Playback timeout `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in device configuration file. Duration verification baseline set to 9 seconds for test comparison | Verify timeout is set appropriately in configuration, duration baseline is 9 seconds |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer MP3 decoder plugins (`mpg123audiodec` or similar), audio output sink configuration, and platform-specific paths. Establish display session via RDKWindowManager. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify environment variables load correctly, MP3 decoder plugins available, audio sink configured successfully, logging initialized without errors |
| 2 | Retrieve Configuration and Construct Playbin Pipeline | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` from device configuration file (default 10 seconds). Retrieve stream variable `audio_src_url_mp3` from MediaValidationVariables.py. Create `playbin` element via . Set URI property via  with MP3 file URL. Set playback flags to  (no video flag for audio-only stream) via  | Verify playbin element created successfully, stream URL configured without errors, flags set for audio-only playback |
| 3 | Configure Audio Sink and Register Callbacks | Playbin automatically selects appropriate audio sink (default is autoaudiosink or configured audio device). Initialize audio streaming by setting up bus message handlers for audio metadata. Note: MP3 is audio-only format, no video sink or frame callbacks required | Verify playbin audio sink configured correctly, pipeline ready for audio stream processing |
| 4 | Transition Pipeline to PLAYING State | Set pipeline state to  via . Poll  until state change completes (). MP3 audio decoder (mpegaudioparse/mpg123audiodec) parses MP3 frames and begins audio decoding | Verify pipeline reaches  without , state transition completes, audio stream begins decoding |
| 5 | Query Stream Duration Using GStreamer Query API | Invoke  to retrieve total MP3 stream duration in nanoseconds. Validate query returns TRUE (success). Verify retrieved duration != -1 (indicates valid, parseable MP3 file). For MP3 streams, `mpegaudioparse` scans ID3v2 metadata and/or calculates duration from bitrate and file size. Convert duration from nanoseconds to seconds via  for logging and comparison | Verify duration query succeeds, returned value is positive integer (not -1), duration formatted correctly |
| 6 | Validate Duration Matches Expected Baseline | Compare queried duration in seconds against expected baseline of 9 seconds. Calculate tolerance as ±250 milliseconds. If queried duration falls within 8.75-9.25 second range, mark duration validation as PASS | Verify duration matches expected 9-second baseline within 250ms tolerance, duration mismatch logged for failure diagnosis |
| 7 | Monitor Playback Position Advancement |  Verify position increments match audio decode rate (no stalls). For audio-only playback, monitor that audio pipeline remains in PLAYING state without buffer underruns or drops | Verify position increments continuously without backward jumps, audio decoding progresses smoothly, no buffer underruns detected |
| 8 | Validate Test Success and Parse Output | Monitor GStreamer bus via  for  (End-of-Stream) or  messages. Verify test framework `checkMediaPipelineTestStatus` output contains strings "Failures: 0" and "Errors: 0" or "failed: 0" indicating clean execution. Execute `DurationParse` custom test step to extract duration from mediapipelinetests output log and verify matches expected 9-second value | Verify no  detected on bus, test status shows zero failures and errors, duration parse step extracts and matches expected value |
| 9 |  Close logging file. Verify all GStreamer resources are freed and memory deallocated | Verify pipeline reaches  cleanly, all objects unreferenced, no resource leaks detected, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3-5 minutes

**Priority:** High

**Release Version:** M121
