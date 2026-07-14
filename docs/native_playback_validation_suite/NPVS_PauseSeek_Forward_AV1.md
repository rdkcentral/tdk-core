## TestCase ID
NATIVE_PLAYBACK_165

## TestCase Name
NPVS_PauseSeek_Forward_AV1

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate pause and forward seek operation on AV1 encoded video streams. The test executes controlled seek operations to a forward position while paused, then resumes playback to verify smooth transition and correct rendering at the seeked location. Confirm playback position advances correctly after seek and frame rendering shows no discontinuities.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | AV1 video stream in DASH container must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`). Stream configured with `test_streams_base_path + "TDK_Asset_DASH_AV1_AAC/master.mpd"` in MediaValidationVariables.py. Stream contains AV1 video and AAC audio in DASH MPD manifest format (for AV1 pause-seek testing) | Verify DASH manifest file is accessible and readable from configured path, AV1 decoder and dashdemux plugins available for stream parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_av1` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "TDK_Asset_DASH_AV1_AAC/master.mpd"` | Verify `video_src_url_av1` resolves to valid AV1 DASH manifest URL, manifest contains valid MPD structure with AV1 codec profile and AdaptationSet elements |
| 4 | Playback Timeout and Seek Position Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) and `NATIVE_PLAYBACK_SEEK_POSITION` (typically a forward position value) must be configured in device configuration file for seek validation | Verify timeout values are set appropriately for pause, seek, and resume operations |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor AV1 decoder libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required environment variables and AV1 decoder plugin paths |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Initialize test environment by sourcing variables from `/opt/TDK/TDK.env` and establish Wayland display session via RDKWindowManager | Verify environment variables load correctly and Wayland display is created |
| 2 | Configure and Execute Test Application | Retrieve configuration and stream URL, then execute `tdk_mediapipelinetests` with test case name, stream URL, and timeout arguments. Load AV1 DASH stream configuration from MediaValidationVariables.py | Verify configuration is retrieved and `tdk_mediapipelinetests` initializes playbin pipeline for AV1 DASH stream |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element with AV1 DASH stream URI, set `westerossink` as video sink, trigger `NULL→READY→PAUSED→PLAYING` state transition, verify `first-video-frame-callback` signal | Verify `playbin` reaches  with first frame rendered from AV1 stream, no  |
| 4 | Execute Pause-Then-Seek Operation |  after reaching intermediate playback position. Query current position via . Invoke  to seek forward to `NATIVE_PLAYBACK_SEEK_POSITION` | Verify pipeline pauses successfully, position query returns valid paused position, forward seek completes within 1 second |
| 5 | Monitor Playback Progress | Resume  after seek. Poll playback position via  at 100ms intervals to verify position advances at normal playback rate (±250ms tolerance per second) | Verify playback resumes from seeked position without stalls, position advances smoothly without backward jumps
| 6 | Validate Frame Rendering | Query `westerossink2192stats` to extract `rendered_frames` increments and `dropped_frames` remains acceptable | Verify frame statistics indicate proper video rendering |
| 7 | Validate Test Success Indicators | Parse GCheck framework output and verify test-specific metrics match expected values | Verify GCheck shows `Failures: 0`, `Errors: 0`, and metrics are correct |
| 8 | Release Pipeline Resources | Set pipeline state to  and release all codec, decoder, and sink resources | Verify pipeline reaches  and system restored to pre-test state |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3-4 minutes

**Priority:** High

**Release Version:** M121
