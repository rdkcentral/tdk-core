## TestCase ID
NATIVE_PLAYBACK_89

## TestCase Name
NPVS_PlayPause_Vorbis

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
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | WebM Vorbis Vorbis stream must be accessible via HTTP(S) (`souphttpsrc`) or local file system (`filesrc`) with matroskademux element with proper manifest/file parsing capability | Verify WebM stream is accessible and contains valid Vorbis and Vorbis representations |
| 3 | Stream Variable Configuration | `video_src_url_vorbis` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "TDK_Asset_Sunrise_VP9_Vorbis.webm"` | Verify `video_src_url_vorbis` resolves to valid location with correct codec support |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in device config | Verify timeout is configured for standard playback |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins and video codec support; Establish Wayland display session via RDKWindowManager; Set up logging file at `/opt/TDK/mediapipeline_test_step.log` | Verify all environment variables load correctly, Wayland display created, logging initialized |
| 2 | Configure and Execute Test Application | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` and stream URL from `video_src_url_vorbis` variable; Execute `mediapipelinetests test_play_pause_pipeline <URL> timeout=<seconds> cycles=3` to prepare play-pause cycling test | Verify mediapipelinetests initializes with WebM stream and cycle count configured |
| 3 | Construct Vorbis WebM Pipeline | Create `playbin` element via ; Configure `uri` property to `video_src_url_vorbis` via ; Set `westerossink` as video sink; Set `autoaudiosink` for Vorbis audio; Trigger state  | Verify playbin reaches , WebM matroskademux active, first frame rendered |
| 4 | Query Video and Audio Stream Properties | Query `westerossink.video-height` and `westerossink.video-width` to confirm stream resolution; Query
-audio` property via  to verify Vorbis stream present; Log stream properties | Verify video dimensions valid; Verify n-audio >= 1 confirming Vorbis stream detected |
| 5 | Execute Play-Pause Cycles | Execute 3+ complete play-pause state transitions via  between  and ; Maintain each state for minimum 1 second to verify stability | Verify all 3+ state transitions complete successfully without errors or timeouts |
| 6 | Monitor Position During Playback State | During PLAYING state, poll  at 100ms intervals to verify position advances at 1x rate (±1 second tolerance per 10 seconds); Verify position never halts or jumps backward | Verify position advances smoothly at consistent 1x playback rate throughout PLAYING periods |
| 7 | Validate Position Halt During Pause | During PAUSED state, poll  at 100ms intervals for minimum 1 second to verify position remains constant (±0 movement); Confirm position does not drift during pause | Verify position remains stationary during PAUSED state with ±0 tolerance |
| 8 | Validate Frame Rendering Statistics | Query `westerossink.stats` to verify `rendered_frames` counter increments ONLY during PLAYING state and remains static during PAUSED state; Verify `dropped_frames` < 1% of rendered_frames throughout all cycles | Verify frame statistics correlate directly with play-pause state transitions |
| 9 | Monitor Bus and Release Resources | Monitor GStreamer message bus via  for errors during all cycles; Call `terminatePipeline(playbin)` to release all resources; Verify test output contains "Failures: 0" confirming all cycles passed | Verify no errors detected on bus; Verify clean shutdown; Verify test passed with 3+ cycles completed |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
