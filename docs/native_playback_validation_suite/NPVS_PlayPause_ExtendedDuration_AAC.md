## TestCase ID
NATIVE_PLAYBACK_173

## TestCase Name
NPVS_PlayPause_ExtendedDuration_AAC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate extended-duration play-pause state management  with H.264 DASH stream containing AAC audio under prolonged playback (>30 seconds). Execute repeated  transitions between `PLAYING` and `PAUSED` states throughout extended playback window. Verify playback position halts completely during PAUSED state and resumes at normal 1x rate (±1 second tolerance) when transitioned back to PLAYING. Monitor frame rendering statistics confirming `rendered_frames` increments only during PLAYING state and remains static during PAUSED, validating state machine stability across long-duration content.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries available |
| 2 | Media Stream Provisioning | DASH stream with MPD manifest must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` in MediaValidationVariables.py. Stream contains H.264 video and AAC audio (DASH container format for extended-duration play-pause testing) | Verify master.mpd manifest file is accessible and readable from configured path, dashdemux plugin available for MPD parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_aac` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` | Verify `video_src_url_aac` resolves to valid DASH manifest URL, manifest contains valid MPD structure with Period, AdaptationSet, Representation elements |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_EXTENDEDDURATION_TIMEOUT` must be configured (default: 60+ seconds) in device config | Verify timeout configured for playback |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD`, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins and codec support; Establish Wayland display session via RDKWindowManager; Set up logging at `/opt/TDK/mediapipeline_test_step.log` | Verify environment loaded, Wayland display created, logging initialized |
| 2 | Configure and Execute Test Application | Retrieve `NATIVE_PLAYBACK_EXTENDEDDURATION_TIMEOUT` and stream URL from `video_src_url_aac` variable; Execute `mediapipelinetests test_play_pause_pipeline <URL> timeout=<seconds> cycles=5` | Verify mediapipelinetests initializes with DASH stream and cycle count configured |
| 3 | Construct H.264 DASH Pipeline | Create `playbin` element via ; Configure `uri` to `video_src_url_aac` via ; Set `westerossink` as video sink; Set `autoaudiosink` for AAC audio;  | Verify playbin reaches , dashdemux active, first frame rendered |
| 4 | Query Video and Audio Properties | Query `westerossink→video-height/width` to confirm resolution; Query `playbin→n-audio` property to verify AAC stream present; Log all stream properties | Verify video dimensions valid; Verify n-audio >= 1 confirming AAC stream detected |
| 5 | Execute 5+ Play-Pause Cycles | Execute 5+ complete play-pause state transitions via  between  and ; Maintain each state for minimum 1 second to verify stability | Verify all 5+ state transitions complete successfully without errors or timeouts |
| 6 | Monitor Position During Playback State | During PLAYING state, poll  at 100ms intervals to verify position advances at 1x rate (±1 second tolerance per 60+ seconds); Verify position never halts or jumps backward | Verify position advances smoothly at consistent 1x playback rate throughout PLAYING periods |
| 7 | Validate Position Halt During Pause | During PAUSED state, poll  at 100ms intervals for minimum 1 second to verify position remains constant (±0 movement); Confirm position does not drift during pause | Verify position remains stationary during PAUSED state with ±0 tolerance |
| 8 | Validate Frame Rendering Statistics | Query `westerossink→stats` to verify `rendered_frames` counter increments ONLY during PLAYING state and remains static during PAUSED state; Verify `dropped_frames` < 1% of rendered_frames throughout all cycles | Verify frame statistics correlate directly with play-pause state transitions |
| 9 | Monitor Bus and Release Resources | Monitor GStreamer message bus via  for errors during all cycles; Call `terminatePipeline(playbin)` to release resources; Verify test output contains "Failures: 0" | Verify no errors detected on bus; Verify clean shutdown; Verify test passed with 5+ cycles completed |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
