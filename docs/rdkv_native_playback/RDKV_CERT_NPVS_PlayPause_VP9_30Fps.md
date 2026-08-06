## TestCase ID
RDKV_NATIVE_PLAYBACK_332

## TestCase Name
RDKV_CERT_NPVS_PlayPause_VP9_30Fps

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate play-pause state management and position control during interactive playback. The test executes repeated transitions between playing state (active rendering) and paused state (halted rendering). When paused, verify playback position halts completely without advancing; when resumed to playing state, verify position advancement resumes at normal rate without gaps. Confirm frame rendering statistics show rendered_frames increments only during play state, demonstrating correct state machine behavior and audio/video synchronization preservation.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries available |
| 2 | Stream Provisioning and Configuration |  MP4 container with VP9 video at 30fps must be accessible via local file system (`filesrc`))<br>or HTTPS (`souphttpsrc`). Stream file configured as `test_streams_base_path + "TDK_Asset_Sunrise_VP9_30fps.mp4"` in MediaValidationVariables.py. Stream contains VP9 video at 30fps and AAC audio (MP4 container format for VP9 30fps play-pause testing))<br>Stream variable `video_src_url_vp9_30fps` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "TDK_Asset_Sunrise_VP9_30fps.mp4"`  | Verify MP4 file is accessible and readable from configured path, qtdemux and VP9 decoder plugins available for playback at 30fps Verify `video_src_url_vp9_30fps` resolves to valid MP4 container file with VP9 video at 30fps and AAC audio data |
| 3 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in device config | Verify timeout configured for playback |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD`, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required variables |
## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins and codec support;<br>Establish Wayland display session via RDKWindowManager; Set up logging at `/opt/TDK/mediapipeline_test_step.log` | Verify environment loaded, Wayland display created, logging initialized |
| 2 | Configure and Execute Test Application | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` and stream URL from `video_src_url_vp9_30fps` variable;<br>Execute `mediapipelinetests test_play_pause_pipeline <URL> timeout=<seconds> cycles=3` | Verify mediapipelinetests initializes with WebM stream and cycle count configured |
| 3 | Construct VP9 WebM Pipeline | Create `playbin` element via `gst_element_factory_make()`; Configure `uri` to `video_src_url_vp9_30fps` via `g_object_set()`;<br>Set `westerossink` as video sink; Set `autoaudiosink` for OPUS audio; Transition to `GST_STATE_PLAYING` | Verify playbin reaches `GST_STATE_PLAYING`, matroskademux active, first frame rendered |
| 4 | Query Video and Audio Properties | Query `g_object_get(westerossink, "video-height")/width` to confirm resolution; Query `g_object_get(playbin, "n-audio")` property to verify OPUS stream present;<br>Log all stream properties | Verify video dimensions valid; Verify n-audio >= 1 confirming OPUS stream detected |
| 5 | Execute 3+ Play-Pause Cycles | Execute 3+ complete play-pause state transitions via `gst_element_set_state()` between `GST_STATE_PLAYING` and `GST_STATE_PAUSED`;<br>Maintain each state for minimum 1 second to verify stability | Verify all 3+ state transitions complete successfully without errors or timeouts |
| 6 | Monitor Position During Playback State | During PLAYING state, poll `gst_element_query_position()` at 100ms intervals to verify position advances at 1x rate ( second tolerance per 10 seconds);<br>Verify position never halts or jumps backward | Verify position advances smoothly at consistent 1x playback rate throughout PLAYING periods |
| 7 | Validate Position Halt During Pause | During PAUSED state, poll `gst_element_query_position()` at 100ms intervals for minimum 1 second to verify position remains constant ( movement);<br>Confirm position does not drift during pause | Verify position remains stationary during PAUSED state with  tolerance |
| 8 | Validate Frame Rendering Statistics | Query `g_object_get(westerossink, "stats")` to verify `rendered_frames` counter increments ONLY during PLAYING state and remains static during PAUSED state;<br>Verify `dropped_frames` < 1% of rendered_frames throughout all cycles | Verify frame statistics correlate directly with play-pause state transitions |
| 9 | Monitor Bus and Release Resources | Monitor GStreamer message bus via `gst_bus_pop()` for errors during all cycles; Call `terminatePipeline(playbin)` to release resources;<br>Verify test output contains "Failures: 0" | Verify no errors detected on bus; Verify clean shutdown; Verify test passed with 3+ cycles completed |
## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121










