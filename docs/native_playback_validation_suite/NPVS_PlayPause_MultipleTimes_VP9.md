## TestCase ID
NATIVE_PLAYBACK_182

## TestCase Name
NPVS_PlayPause_MultipleTimes_VP9

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify stress-tested play-pause operations on VP9 stream . The test executes 3+ complete play-pause cycles by repeatedly alternating between GST_STATE_PLAYING and GST_STATE_PAUSED states to validate state machine stability, resource cleanup, and playback recovery under stress conditions. Verify playback position advances at 1x rate (±1 second) during play and remains constant (±0 movement) during pause, validate frame rendering statistics via westerossink→stats show rendered_frames increment only during play state, and detect no GStreamer errors or buffer starvation issues throughout all stress cycles.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | WebM VP9 OPUS stream must be accessible via HTTP(S) (`souphttpsrc`) or local file system (`filesrc`) with dashdemux (WebM format) element with proper manifest or file parsing capability. Stream path: `DASH_VP9_OPUS_WebM/master.mpd` | Verify WebM stream is accessible and contains valid VP9 and OPUS representations |
| 3 | Stream Variable Configuration | `video_src_url_vp9` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "DASH_VP9_OPUS_WebM/master.mpd"` | Verify `video_src_url_vp9` resolves to valid location with correct codec support |
| 4 | Stress Test Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) and `NATIVE_PLAYBACK_STRESS_REPEAT_COUNT` (default: 3) must be configured in device config for play-pause operation duration and cycle repetition | Verify timeout configured for playback operations and stress repeat count configured for 3+ cycles |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, Wayland display is created successfully, logging initialized without errors |
| 2 | Configure Stress Test Application | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (timeout for each play/pause operation, default: 10 seconds) and `NATIVE_PLAYBACK_STRESS_REPEAT_COUNT` (number of play-pause cycles, default: 3); Retrieve stream URL from `video_src_url_vp9` variable; Construct operations string with `play:<timeout>,pause:<timeout>` repeated 3+ times; Execute `mediapipelinetests test_trickplay <URL> operations=<operations_string>` to prepare stress test | Verify mediapipelinetests initializes with WebM stream and stress operation parameters (operations string, repeat count) correctly configured |
| 3 | Construct VP9 WebM Pipeline and Initiate Playing State | Create `playbin` element via ; Configure `uri` property to `video_src_url_vp9` via ; Set `westerossink` as video sink via ; Configure `autoaudiosink` for OPUS audio via ; Trigger state  via  | Verify playbin reaches , WebM dashdemux (WebM format) active and parsing stream, first frame rendered via first-video-frame-callback signal, no  on bus |
| 4 | Query Initial Stream Properties | Query `westerossink.video-height` and `westerossink.video-width` via  to confirm stream resolution; Query
-audio` property via  to verify OPUS stream present; Query playback duration via ; Log all stream properties | Verify video dimensions valid; Verify n-audio >= 1 confirming OPUS stream detected; Verify stream duration retrieved successfully |
| 5 | Execute Play-Pause Stress Cycles | For each cycle iteration (repeated 3+ times): Execute PLAY operation by setting pipeline to  via  and maintaining for NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT seconds; Then execute PAUSE operation by setting pipeline to  via  and maintaining for NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT seconds; Repeat 3+ complete play-pause cycles | Verify all 3+ play-pause cycle transitions complete successfully without errors, timeouts, or resource exhaustion; Verify pipeline state changes properly reflect via  |
| 6 | Monitor Playback Position During Play State | During each PLAYING state interval, poll  at 100ms intervals to verify position advances at 1x rate (±1 second tolerance per timeout window); Verify position never halts or exhibits backward jumps during play intervals | Verify position increments smoothly at consistent 1x playback rate throughout all PLAYING periods; Verify no position stalls or anomalies detected |
| 7 | Validate Position Halt During Pause State | During each PAUSED state interval, poll  at 100ms intervals for minimum 1 second to verify position remains constant (±0 movement); Confirm position does not drift or change during pause intervals across all stress cycles | Verify position remains completely stationary during all PAUSED state periods with ±0 tolerance; Verify no position drift detected despite multiple pause-resume cycles |
| 8 | Validate Frame Rendering Statistics Under Stress | Query `westerossink.stats` at 1-second intervals during all play-pause cycles to verify `rendered_frames` counter increments ONLY during PLAYING state and remains static during PAUSED state; Verify `dropped_frames` < 1% of rendered_frames throughout all stress cycles; Monitor frame statistics correlate directly with state transitions | Verify frame statistics show rendered_frames increment during play and remain static during pause for all 3+ cycles; Verify dropped frame rate acceptable throughout stress test |
| 9 | Monitor GStreamer Bus and Release Resources | Monitor GStreamer message bus via  for , , or  messages during all cycles; Call `terminatePipeline(playbin)` to set state to  via  and release all GStreamer objects (playbin, demuxer, westerossink, audioSink); Verify test output contains "Failures: 0" and "Errors: 0" or "failed: 0" confirming all stress cycles passed | Verify no errors detected on GStreamer bus throughout all stress cycles; Verify clean pipeline shutdown reaching ; Verify test output shows successful completion with 0 failures for 3+ play-pause stress cycles |## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
