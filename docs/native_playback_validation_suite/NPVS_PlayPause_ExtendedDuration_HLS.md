## TestCase ID
NATIVE_PLAYBACK_176

## TestCase Name
NPVS_PlayPause_ExtendedDuration_HLS

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate HLS streaming format parsing and pipeline initialization.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | HLS stream with M3U8 playlist must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "HLS_H264_AAC/master.m3u8"` in MediaValidationVariables.py. Stream contains H.264 video and AAC audio (HLS container format for extended-duration play-pause testing) | Verify master.m3u8 playlist file is accessible and readable from configured path, hlsdemux plugin available for M3U8 parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_hls` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "HLS_H264_AAC/master.m3u8"` | Verify `video_src_url_hls` resolves to valid HLS manifest URL, playlist contains valid M3U8 structure with variant streams and segment references |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_EXTENDEDDURATION_TIMEOUT` must be configured (default: 60+ seconds) in device config | Verify timeout is configured for extended duration playback |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |
## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins and video codec support; Establish Wayland display session via RDKWindowManager; Set up logging file at `/opt/TDK/mediapipeline_test_step.log` | Verify all environment variables load correctly, Wayland display created, logging initialized |
| 2 | Configure and Execute Test Application | Retrieve `NATIVE_PLAYBACK_EXTENDEDDURATION_TIMEOUT` and stream URL from `video_src_url_hls` variable; Execute `mediapipelinetests test_play_pause_pipeline <URL> timeout=<seconds> cycles=5` to prepare play-pause cycling test | Verify mediapipelinetests initializes with HLS stream and cycle count configured |
| 3 | Construct H.264 HLS Pipeline | Create `playbin` element via `gst_element_factory_make()`; Configure `uri` property to `video_src_url_hls` via `g_object_set()`; Set `westerossink` as video sink; Set `autoaudiosink` for AAC audio; Trigger state transition to `GST_STATE_PLAYING` | Verify playbin reaches `GST_STATE_PLAYING`, HLS hlsdemux active, first frame rendered |
| 4 | Query Video and Audio Stream Properties | Query `westerossinkâ†’video-height` and `westerossinkâ†’video-width` to confirm stream resolution; Query 
-audio` property via `g_object_get()` to verify AAC stream present; Log stream properties | Verify video dimensions valid; Verify n-audio >= 1 confirming AAC stream detected |
| 5 | Execute Play-Pause Cycles | Execute 5+ complete play-pause state transitions via `gst_element_set_state()` between `GST_STATE_PLAYING` and `GST_STATE_PAUSED`; Maintain each state for minimum 1 second to verify stability | Verify all 5+ state transitions complete successfully without errors or timeouts |
| 6 | Monitor Position During Playback State | During PLAYING state, poll `gst_element_query_position()` at 100ms intervals to verify position advances at 1x rate (Â±1 second tolerance per 60+ seconds); Verify position never halts or jumps backward | Verify position advances smoothly at consistent 1x playback rate throughout PLAYING periods |
| 7 | Validate Position Halt During Pause | During PAUSED state, poll `gst_element_query_position()` at 100ms intervals for minimum 1 second to verify position remains constant (Â±0 movement); Confirm position does not drift during pause | Verify position remains stationary during PAUSED state with Â±0 tolerance |
| 8 | Validate Frame Rendering Statistics | Query `westerossinkâ†’stats` to verify `rendered_frames` counter increments ONLY during PLAYING state and remains static during PAUSED state; Verify `dropped_frames` < 1% of rendered_frames throughout all cycles | Verify frame statistics correlate directly with play-pause state transitions |
| 9 | Monitor Bus and Release Resources | Monitor GStreamer message bus via `gst_bus_pop()` for errors during all cycles; Call `terminatePipeline(playbin)` to release all resources; Verify test output contains "Failures: 0" confirming all cycles passed | Verify no errors detected on bus; Verify clean shutdown; Verify test passed with 5+ cycles completed |
## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
