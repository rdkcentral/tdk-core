## TestCase ID
NATIVE_PLAYBACK_62

## TestCase Name
NPVS_PlaySeek_Forward_HEVC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate forward seek operation on H.265 DASH streams. The test verifies accurate positioning to the target seek point within ±1 second tolerance, seamless playback recovery after seek, frame rendering without interruption, and error-free playback.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | DASH H.265 stream must be accessible via HTTP (`souphttpsrc`) or local file system (`filesrc`) with dashdemux element. Stream path: `DASH_HEVC_AAC/master.mpd` | Verify DASH stream is accessible and contains valid H.265 and AAC representations |
| 3 | Stream Variable Configuration | `video_src_url_hevc` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "DASH_HEVC_AAC/master.mpd"` | Verify `video_src_url_hevc` resolves to valid location with correct codec support |
| 4 | Seek Test Configuration | NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT (default: 10 seconds) and NATIVE_PLAYBACK_SEEK_POSITION (default: 20 seconds for forward seek target position) must be configured in device config for forward seek operation timing and target position | Verify seek timeout configured for forward seek duration and seek target position configured for forward seek operation |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, Wayland display is created successfully, logging initialized without errors |
| 2 | Configure Seek Test Application | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (playback duration for each seek operation), `NATIVE_PLAYBACK_SEEK_POSITION` (target position for forward seek, default 20 seconds); Retrieve stream URL from `video_src_url_hevc` variable; Construct seek operation string with `seek:timeout:position`; Execute `mediapipelinetests test_trickplay <URL> operations=<seek_string>` to prepare seek test | Verify mediapipelinetests initializes with DASH stream and seek operation parameters correctly configured |
| 3 | Construct H.265 DASH Pipeline and Initiate Playing State | Create `playbin` element via ; Configure `uri` property to `video_src_url_hevc` via ; Set `westerossink` as video sink (or `autoaudiosink` for audio-only) via ; Trigger state  via  | Verify playbin reaches , DASH dashdemux active and parsing stream, first frame rendered via first-video-frame-callback signal (or first audio sample for audio-only), no  on bus |
| 4 | Query Initial Stream Properties | Query `westerossink→video-height` and `westerossink→video-width` via  to confirm stream resolution (skip for audio-only); Query
-audio` property via  to verify AAC stream present; Query playback duration via ; Log all stream properties | Verify video dimensions valid; Verify n-audio >= 1 confirming AAC stream detected; Verify stream duration retrieved successfully |
| 5 | Execute Forward Seek Operation | During active playback, invoke  with `NORMAL_PLAYBACK_RATE`, , , , and target seek position via ; Pipeline automatically flushes pending buffers and transitions to specified position; Wait for async state change to complete | Verify  call succeeds, pipeline transitions to new position, no  on bus during seek |
| 6 | Validate Seek Position Accuracy | Poll  at 100ms intervals immediately after seek completion (for minimum 2 seconds) to verify current position matches seek target within ±1 second tolerance; Monitor position should not exceed 1 second difference from target seek position | Verify position reaches target within ±1 second; Verify position does not overshoot or undershoot beyond tolerance |
| 7 | Monitor Frame Rendering After Seek | Query westerossink→stats at 1-second intervals to verify `rendered_frames` counter increases after seek (pipeline recovers and resumes rendering); Verify `dropped_frames` < 1% of rendered_frames after seek operation; Confirm frame statistics show seamless recovery from seek state | Verify westerossink→stats to verify rendered_frames and dropped_frames show activity after seek, frame rendering resumes without extended stalls, dropped frame rate acceptable |
| 8 | Monitor GStreamer Bus for Errors | Monitor GStreamer message bus via  for , , or  messages during and after seek operations; Continue playback for full duration per timeout configuration; Log any error messages for analysis | Verify no errors detected on GStreamer bus during seek operation, playback continues normally after seek to completion |
| 9 | Monitor Playback Completion and Release Resources | If EOS received, verify test framework detects end-of-stream; Call `terminatePipeline(playbin)` to set state to  via  and release all GStreamer objects (playbin, demuxer, westerossink, audioSink); Verify test output contains "Failures: 0" and "Errors: 0" or "failed: 0" confirming seek test passed | Verify clean pipeline shutdown reaching , all resources properly released, test output shows successful completion with 0 failures for forward seek operation |## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
