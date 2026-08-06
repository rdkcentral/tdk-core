## TestCase ID
RDKV_NATIVE_PLAYBACK_174

## TestCase Name
RDKV_CERT_NPVS_PlayPause_ExtendedDuration_DASH

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate Dynamic Adaptive Streaming over HTTP (DASH) playback with extended duration content through sustained play-pause cycling. Execute multiple play-pause state cycles to verify pipeline maintains stability during repeated transitions between PLAYING and PAUSED states over extended playback duration without stalls, buffer underruns, or resource exhaustion. Monitor frame rendering statistics and verify position synchronization across segment boundaries.r playback position advancement to verify position increments smoothly at 1x rate during PLAYING state and remains stationary during PAUSED state. Query property to validate frame rendering statistics (rendered_frames increments consistently, dropped_frames < 1% throughout extended session). Verify DASH dashdemux plugin successfully parses MPD manifest, adapts to bitrate changes, and seamlessly switches between variant streams during extended playback without interruption or synchronization loss.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration |  DASH stream with MPD manifest must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` in MediaValidationVariables.py. Stream contains H.264 video and AAC audio (DASH container format for extended-duration play-pause testing))<br>Stream variable `video_src_url_dash` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"`  | Verify master.mpd manifest file is accessible and readable from configured path, dashdemux plugin available for MPD parsing Verify `video_src_url_dash` resolves to valid DASH manifest URL, manifest contains valid MPD structure with Period, AdaptationSet, Representation elements |
| 3 | Playback Timeout Configuration | `NATIVE_PLAYBACK_EXTENDEDDURATION_TIMEOUT` must be configured (default: 60+ seconds) in device config | Verify timeout is configured for extended duration playback |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |
## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins and video codec support;<br>Establish Wayland display session via RDKWindowManager; Set up logging file at `/opt/TDK/mediapipeline_test_step.log` | Verify all environment variables load correctly, Wayland display created, logging initialized |
| 2 | Configure and Execute Test Application | Retrieve `NATIVE_PLAYBACK_EXTENDEDDURATION_TIMEOUT` and stream URL from `video_src_url_dash` variable;<br>Execute `mediapipelinetests test_play_pause_pipeline <URL> timeout=<seconds> cycles=5` to prepare play-pause cycling test | Verify mediapipelinetests initializes with DASH stream and cycle count configured |
| 3 | Construct H.264 DASH Pipeline | Create `playbin` element via `gst_element_factory_make()`; Configure `uri` property to `video_src_url_dash` via `g_object_set()`;<br>Set `westerossink` as video sink; Set `autoaudiosink` for AAC audio; Trigger state transition to `GST_STATE_PLAYING` | Verify playbin reaches `GST_STATE_PLAYING`, DASH dashdemux active, first frame rendered |
| 4 | Query Video and Audio Stream Properties | Query `g_object_get(westerossink, "video-height")` and `g_object_get(westerossink, "video-width")` to confirm stream resolution;<br>Query `g_object_get(playbin, "n-audio")` property via `g_object_get()` to verify AAC stream present; Log stream properties | Verify video dimensions valid; Verify n-audio >= 1 confirming AAC stream detected |
| 5 | Execute Play-Pause Cycles | Execute 5+ complete play-pause state transitions via `gst_element_set_state()` between `GST_STATE_PLAYING` and `GST_STATE_PAUSED`;<br>Maintain each state for minimum 1 second to verify stability | Verify all 5+ state transitions complete successfully without errors or timeouts |
| 6 | Monitor Position During Playback State | During PLAYING state, poll `gst_element_query_position()` at 100ms intervals to verify position advances at 1x rate ( second tolerance per 60+ seconds);<br>Verify position never halts or jumps backward | Verify position advances smoothly at consistent 1x playback rate throughout PLAYING periods |
| 7 | Validate Position Halt During Pause | During PAUSED state, poll `gst_element_query_position()` at 100ms intervals for minimum 1 second to verify position remains constant ( movement);<br>Confirm position does not drift during pause | Verify position remains stationary during PAUSED state with  tolerance |
| 8 | Validate Frame Rendering Statistics | Query `g_object_get(westerossink, "stats")` to verify `rendered_frames` counter increments ONLY during PLAYING state and remains static during PAUSED state;<br>Verify `dropped_frames` < 1% of rendered_frames throughout all cycles | Verify frame statistics correlate directly with play-pause state transitions |
| 9 | Monitor Bus and Release Resources | Monitor GStreamer message bus via `gst_bus_pop()` for errors during all cycles; Call `terminatePipeline(playbin)` to release all resources;<br>Verify test output contains "Failures: 0" confirming all cycles passed | Verify no errors detected on bus; Verify clean shutdown; Verify test passed with 5+ cycles completed |
## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121









