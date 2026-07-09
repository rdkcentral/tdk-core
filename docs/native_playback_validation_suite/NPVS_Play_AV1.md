## TestCase ID
NATIVE_PLAYBACK_04

## TestCase Name
NPVS_Play_AV1

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate AV1 video codec with AAC audio  using DASH streaming.  Query video dimensions and audio stream count and 
-audio` properties. Execute 10-second playback monitoring position advancement, frame rendering via `westerossinkâ†’stats`, and verify audio-video synchronization throughout stream.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | DASH AV1 AAC stream (`master.mpd`) must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`) element with `dashdemux` capable of parsing DASH container  | Verify DASH stream is accessible and contains valid AV1 and AAC representations |
| 3 | Stream Variable Configuration | `video_src_url_av1` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "TDK_Asset_DASH_AV1_AAC/master.mpd"` | Verify `video_src_url_av1` resolves to valid DASH location with correct codec support |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout configured for standard playback (10 seconds) | Verify `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` is set to 10 seconds in configuration file | Verify timeout set to minimum 10 seconds; Verify AV-status check configuration |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` | Verify all environment variables load correctly, Wayland display is created successfully, logging initialized without errors |
| 2 | Configure and Execute Test Application | Retrieve configuration values for `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` from device config; Retrieve stream URL from `video_src_url_av1` variable; Execute `mediapipelinetests test_generic_playback <DASH_URL> timeout=<seconds>` | Verify mediapipelinetests initializes with AV1 DASH stream and timeout parameters |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element via  with video_src_url_av1 URI; Configure `uri` property to video_src_url_av1 manifest/file via ; Set `video-sink` property to `westerossink` via ; Configure `autoaudiosink` for AAC audio; Trigger state  to  via ; Monitor for `first-video-frame-callback` signal | Verify playbin reaches  with first frame decoded, DASH manifest/file parsed successfully, no  |
| 4 | Query Video and Audio Stream Properties | Query video dimensions via  and `westerossinkâ†’video-width`; Query audio stream count via  to verify AAC stream presence; Log extracted properties | Verify video dimensions valid; Verify n-audio >= 1 confirming AAC stream present |
| 5 | Play Stream for Configured Timeout | Execute continuous playback via PlaySeconds(playbin, play_timeout) or equivalent for configured timeout (default 10 seconds); Monitor playback position via  at 100ms intervals to verify position advances at 1x rate | Verify playback position advances consistently at 1x rate (±1 second tolerance), no stalls or backward jumps detected |
| 6 | Validate Frame Rendering and Statistics | Poll `westerossinkâ†’stats` to verify `rendered_frames` increments indicating continuous video rendering; Verify `dropped_frames` < 1% of rendered_frames throughout playback; Log frame statistics | Verify frame statistics indicate proper video rendering at AV1; Verify dropped frame rate acceptable |
| 7 | Monitor GStreamer Bus and Detect EOS | Monitor GStreamer message bus via  to detect , , or  messages; Verify no error messages indicating codec decoding failures or stream parsing issues | Verify no decoder errors or format errors on bus; Verify clean playback without glitches or interruptions |
| 8 | Release Pipeline Resources | Call `terminatePipeline(playbin)` to set state to  via  and release all GStreamer objects (playbin, DASH demuxer, westerossink, audio sink, bus); Verify cleanup completes successfully without resource leaks | Verify pipeline reaches ; Verify all resources released; Verify test output contains "Failures: 0" and "Errors: 0" or "failed: 0" |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
