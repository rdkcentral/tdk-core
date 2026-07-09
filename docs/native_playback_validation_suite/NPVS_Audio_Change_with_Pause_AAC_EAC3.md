## TestCase ID
NATIVE_PLAYBACK_129

## TestCase Name
NPVS_Audio_Change_with_Pause_AAC_EAC3

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate dynamic audio codec switching between AAC and EAC3 with pause operations during playback. The test switches between different audio codec types in a multi-codec stream with pause/resume during continuous video playback. Verify audio rendering quality, position synchronization, and codec switching timing accuracy without audio/video interruption.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | Multi-codec stream containing both AAC and EAC3 audio tracks must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`) with DASH manifest. Stream configured as `test_streams_base_path + "MultiCodecStreams/stream_with_aac_eac3_pause.mpd"` in MediaValidationVariables.py | Verify multi-codec DASH stream accessible, both AAC and EAC3 audio tracks present and parseable |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_aac_eac3_pause` configured in `MediaValidationVariables.py` with DASH manifest containing AAC and EAC3 audio tracks | Verify `video_src_url_aac_eac3_pause` resolves to valid multi-codec stream with dual audio tracks |
| 4 | Device Configuration Parameters | Configuration parameters `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default 10 seconds per codec) must be retrievable from device configuration | Verify device config returns valid timeout  |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables, Wayland display active |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland configuration. Establish Wayland display session via RDKWindowManager. Initialize logging to `/opt/TDK/mediapipeline_test_step.log` | Verify environment variables load without errors, Wayland display active, logging initialized |
| 2 | Configure Test Parameters and Load Multi-Codec Stream | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` from device. Build `mediapipelinetests` command with test_name="test_playback_audio_change_with_pause", stream_url=video_src_url_aac_eac3_pause, timeout=N | Verify device config retrieved successfully, command constructed with correct parameters |
| 3 | Create Playbin Pipeline and Load Multi-Codec Stream | Create `playbin` element via . Set `uri` property to multi-codec DASH stream URL via . Trigger state transitions to  via  | Verify playbin created, URI configured to multi-codec DASH stream, pipeline transitions to PLAYING |
| 4 | Retrieve and Verify Multiple Audio Tracks | Query playbin to determine number of audio streams via . Verify n-audio >= 2 (confirming AAC and EAC3 tracks present). Query current audio index via  to identify default (AAC) track | Verify n-audio returns at least 2, current-audio successfully retrieved (typically 0 for first codec) |
| 5 | Verify Initial AAC Audio Playback and Retrieve Audio-Tags | Emit "get-audio-tags" signal for default audio track via . Parse tag list using  to identify codec name (AAC). Log audio-tags including codec type, sample rate, channels as baseline. Poll playback position for 5-10 seconds to verify AAC audio plays without interruption | Verify audio-tags successfully retrieved showing AAC codec (e.g., audio/mpeg), playback position advances linearly, no audio glitches or stalls |
| 6 | Pause Playback Before Codec Switch | Issue  to pause playback. Verify state transition succeeded via  confirming state equals . Query position via  to record pause point. Verify video and audio outputs frozen | Verify playback paused, state confirmed PAUSED, position query succeeds, video/audio output frozen with no artifacts |
| 7 | Switch to EAC3 Codec During Pause and Flush Pipeline | While in PAUSED state, set `current-audio` property via  to switch to EAC3 track (index 1). Verify switch via  confirming value equals 1. Query pause point position. Flush pipeline via  to clear buffered AAC data. Wait 2 seconds for EAC3 buffer fill. Reset underflow flag | Verify current-audio property set to 1, seek-flush from paused state executes successfully, 2-second wait completes, underflow flag reset |
| 8 | Resume Playback with New EAC3 Codec | Issue  to resume playback with EAC3 codec active. Verify state transition succeeded. Emit "get-audio-tags" signal for EAC3 track via . Parse tags to confirm EAC3 codec (e.g., audio/x-eac3). Log audio-tags. Poll playback position for 5-10 seconds to verify smooth resume at pause point with EAC3 audio | Verify playback resumes from pause point, audio-tags show EAC3 codec (different from AAC), position advances smoothly from resume point |
| 9 | Monitor EAC3 Playback and Validate Continuity | Continue  Verify position advances linearly with no backward jumps. Monitor bus for `pts-error-callback` signals (should be none). Check for audio underflow conditions (should be none). Verify video playback continues uninterrupted | Verify EAC3 position advances smoothly, no pts-error or underflow signals, video continues playing, audio output clear and artifact-free |
| 10 | Validate Pause-Resume Codec Switch Support and Release Resources | Review logged audio-tags from both codec playbacks. Verify codec identity confirmed: Step 5 shows AAC, Step 8 shows EAC3 (distinctly different). Verify pause-resume transition maintained correct position and audio output. Verify test output shows `Failures: 0`, `Errors: 0`. Set pipeline to  via . Call . Free allocated memory and close logging file | Verify audio-tags logs confirm both codecs properly identified, pause-resume switch successful, test completed with zero failures/errors, pipeline NULL, all resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
