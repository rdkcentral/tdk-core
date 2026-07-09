## TestCase ID
NATIVE_PLAYBACK_69

## TestCase Name
NPVS_PlaySeek_Forward_Only_Audio_MP3

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate forward seek operation during audio-only MP3 playback. The test verifies accurate positioning to the target seek point within ±1 second tolerance, seamless playback recovery after seek, audio rendering without interruption, and error-free playback.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries including GStreamer plugins and audio sink support | Verify TDK_Package is installed, binary is executable (`/usr/bin/tdk_mediapipelinetests` or equivalent), and audio processing libraries available |
| 2 | Audio Stream Provisioning | MP3 audio/mpeg stream must be accessible  with local file path or HTTP stream accessible to mpegaudioparse element. Stream file path: `test_streams_base_path + "TDK_Asset_Sunrise_MP3.mp3"` from MediaValidationVariables.py | Verify MP3 audio/mpeg stream file is accessible, readable, and contains valid audio codec data with proper headers |
| 3 | Stream Variable Configuration | `audio_src_url_mp3` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "TDK_Asset_Sunrise_MP3.mp3"` with accessible URL or local file path | Verify `audio_src_url_mp3` variable resolves to valid, accessible audio stream location |
| 4 | Audio Playback Configuration | NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT (default: 10 seconds) and NATIVE_PLAYBACK_SEEK_POSITION (default: 20 seconds for forward seek target) must be configured in device config for audio seek operation timing | Verify seek timeout and target position configured correctly; For audio-only: no video timeout or frame rate checks are applied |
| 5 | Platform-Specific Audio Environment | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, , `LD_LIBRARY_PATH` with audio libraries and ) must be defined in `/opt/TDK/TDK.env`; Optional: NATIVE_PLAYBACK_USE_AUDIO_SINK configured for SoC-specific audio sink (default: autoaudiosink) | Verify `/opt/TDK/TDK.env` contains all audio-specific environment variables; Audio sink available (autoaudiosink or configured tdkaudiosink) |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment and Load Configuration | Source `/opt/TDK/TDK.env` to load GStreamer plugins (), audio sink libraries (`LD_LIBRARY_PATH`, `LD_PRELOAD`), and Wayland display configuration (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`). Establish Wayland display session via RDKWindowManager or westeros compositor. Create logging file at `/opt/TDK/mediapipeline_test_step.log` for execution trace. Retrieve device configuration values:(default: "no"), `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds), `NATIVE_PLAYBACK_SEEK_POSITION` (default: 20 seconds) | Verify all environment variables load correctly; Wayland display created successfully; Device config parameters retrieved; Logging file initialized |
| 2 | Configure Audio Seek Test Application | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` for playback duration per operation and `NATIVE_PLAYBACK_SEEK_POSITION` for forward seek target position from device config. Retrieve `audio_src_url_mp3` stream URL from MediaValidationVariables library. Construct seek operation string with format: `seek:<timeout_seconds>:<seek_target_seconds>` (example: `seek:10:20`). Build complete command: `mediapipelinetests test_trickplay <audio_stream_url> operations=<seek_string> only_audio` | Verify mediapipelinetests command constructed correctly with audio stream URL, seek parameters, and `only_audio` flag |
| 3 | Construct MP3 Audio Pipeline with Playbin and Audio-Only Mode | Execute mediapipelinetests with `test_trickplay` test case. Internally: Create `playbin` element via  and configure `uri` property to stream URL via . Set `westerossink` as video-sink via  (required for internal pipeline even in audio-only mode). Configure `autoaudiosink` or device-configured audio sink via . Pass `only_audio` flag to framework which disables video validation: sets `checkPTS=false` and `use_westerossink_fps=false`. Set `async-handling` to true | Verify playbin created and configured; Video sink connected (validation skipped); Audio sink (`autoaudiosink` or `tdkaudiosink`) connected and configured; only_audio flag applied to disable video checks |
| 4 | Transition Pipeline to PLAYING State and Verify Audio Activation | Call  to transition pipeline. Wait for state change completion via . Monitor GStreamer bus via  for state transition messages (GST_MESSAGE_STATE_CHANGED). Verify `mpegaudioparse element` active and parsing audio stream from source. Register audio pad and verify caps via  showing valid audio codec, sample rate, and channel count | Verify playbin reaches ; `mpegaudioparse element` active and processing stream; Audio pad connected with valid caps; No GST_MESSAGE_ERROR on bus |
| 5 | Query Initial Audio Stream Properties | Query playback duration via  to determine stream length in nanoseconds. Convert to seconds: duration_sec = duration / GST_SECOND. Query audio properties:  returns caps containing format, sample rate (typically 48000 Hz), and channels (1-6). Query 
-audio` property via  to confirm audio track count >= 1. Log all stream properties (format, sample rate, channels, duration) | Verify stream duration successfully queried and >= 30 seconds for seeking; Verify n-audio >= 1 confirming audio stream present; Verify audio pad caps show valid sample rate and channels; No video properties queried (audio-only mode) |
| 6 | Execute Forward Seek Operation and Wait for Completion | During active playback at current position, invoke  with seek_position_ns = NATIVE_PLAYBACK_SEEK_POSITION * GST_SECOND. GST_SEEK_FLAG_FLUSH causes pending buffers to be flushed and pipeline to transition to target position. For audio-only mode: Monitor GStreamer bus for , , , and  messages with 2-second timeout via . Continue when  received (indicates seek completion) | Verify  call returns TRUE; Pipeline transitions to target position; GST_MESSAGE_ASYNC_DONE received within 2 seconds confirming seek completion; No GST_MESSAGE_ERROR on bus |
| 7 | Validate Seek Position Accuracy Within Tolerance | After seek completion,  Calculate position_seconds = current_position / GST_SECOND. Verify |position_seconds - NATIVE_PLAYBACK_SEEK_POSITION| <= 1.0 second (±1 second tolerance as per PlaybackValidation function). Track position drift: position should not move backward, should advance at ~1.0 seconds per real-time second after seek stabilization. Log each position query result with timestamp | Verify position reaches target within ±1 second tolerance; Verify position does not overshoot (> +1.5 seconds) or undershoot (< -1.5 seconds); Verify no position backward jumps or stalls detected |
| 8 | Validate Audio Playback Continuity After Seek | For audio-only: Monitor playback position continuity via repeated  calls every 100ms for 2 seconds. Calculate position_jump = current_position - previous_position for each interval; all jumps should be ~0.1 seconds (±0.05 tolerance). Any jump < 0.05 or > 0.15 indicates audio stall or drop. Monitor GStreamer bus for  or  that indicate audio decode/rendering issues. Query audio pad buffer level if available to confirm data flowing. Continue playback monitoring for full NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT duration to ensure sustained audio output | Verify position advances continuously with expected rate (~0.1s per 100ms poll); Verify no audio stalls detected; No error/warning messages on bus; Audio rendering continues without interruption |
| 9 | Monitor Pipeline EOS and Release Resources | Continue playback until `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` expires or  detected on bus via . When test duration completes: Set pipeline to  via . Call  to release playbin element reference. Release all GStreamer objects and close logging file. Verify mediapipelinetests output contains success indicators: "Failures: 0" and "Errors: 0" or "failed: 0" | Verify playback continues for specified timeout without early termination;  reached cleanly; All GStreamer resources released; Test output shows "Failures: 0" and "Errors: 0" or "failed: 0" confirming forward seek test PASSED |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
