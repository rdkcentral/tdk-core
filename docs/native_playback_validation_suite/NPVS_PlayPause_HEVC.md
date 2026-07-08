## TestCase ID
NATIVE_PLAYBACK_92

## TestCase Name
NPVS_PlayPause_HEVC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate play-pause state transitions during playback. The test verifies pausing halts rendering and position, resuming continues from pause point without gaps, and frame rendering reflects state changes.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries available |
| 2 | Media Stream Provisioning | DASH stream with MPD manifest containing HEVC video must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd"` in MediaValidationVariables.py. Stream contains HEVC (H.265) video and AAC audio (DASH container format for HEVC play-pause testing) | Verify master.mpd manifest file is accessible and readable from configured path, dashdemux and HEVC decoder plugins available for parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_hevc` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd"` | Verify `video_src_url_hevc` resolves to valid DASH manifest URL with HEVC content, manifest contains valid MPD structure with HEVC codec profile |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in device config | Verify timeout configured for playback |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD`, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins and codec support; Establish Wayland display session via RDKWindowManager; Set up logging at `/opt/TDK/mediapipeline_test_step.log` | Verify environment loaded, Wayland display created, logging initialized |
| 2 | Configure and Execute Test Application | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` and stream URL from `video_src_url_hevc` variable; Execute `mediapipelinetests test_play_pause_pipeline <URL> timeout=<seconds> cycles=3` | Verify mediapipelinetests initializes with DASH stream and cycle count configured |
| 3 | Construct H.265 DASH Pipeline | Create `playbin` element via ; Configure `uri` to `video_src_url_hevc` via ; Set `westerossink` as video sink; Set `autoaudiosink` for AAC audio;  | Verify playbin reaches , dashdemux active, first frame rendered |
| 4 | Query Video and Audio Properties | Query `westerossink→video-height/width` to confirm resolution; Query `playbin→n-audio` property to verify AAC stream present; Log all stream properties | Verify video dimensions valid; Verify n-audio >= 1 confirming AAC stream detected |
| 5 | Execute 3+ Play-Pause Cycles | Execute 3+ complete play-pause state transitions via  between  and ; Maintain each state for minimum 1 second to verify stability | Verify all 3+ state transitions complete successfully without errors or timeouts |
| 6 | Monitor Position During Playback State | During PLAYING state, poll  at 100ms intervals to verify position advances at 1x rate (±1 second tolerance per 10 seconds); Verify position never halts or jumps backward | Verify position advances smoothly at consistent 1x playback rate throughout PLAYING periods |
| 7 | Validate Position Halt During Pause | During PAUSED state, poll  at 100ms intervals for minimum 1 second to verify position remains constant (±0 movement); Confirm position does not drift during pause | Verify position remains stationary during PAUSED state with ±0 tolerance |
| 8 | Validate Frame Rendering Statistics | Query `westerossink→stats` to verify `rendered_frames` counter increments ONLY during PLAYING state and remains static during PAUSED state; Verify `dropped_frames` < 1% of rendered_frames throughout all cycles | Verify frame statistics correlate directly with play-pause state transitions |
| 9 | Monitor Bus and Release Resources | Monitor GStreamer message bus via  for errors during all cycles; Call `terminatePipeline(playbin)` to release resources; Verify test output contains "Failures: 0" | Verify no errors detected on bus; Verify clean shutdown; Verify test passed with 3+ cycles completed |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 1-2 minutes

**Priority:** High

**Release Version:** M121
