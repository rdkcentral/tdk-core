## TestCase ID
NATIVE_PLAYBACK_120

## TestCase Name
NPVS_Audio_Change_AC3_EAC3

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate dynamic audio codec switching between AC3 and EAC3 during playback. The test switches between different audio codec types in a multi-codec stream while maintaining continuous video playback. Verify audio rendering quality, position synchronization, and codec switching timing accuracy without audio/video interruption.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | Multi-codec stream containing both AC3 and EAC3 audio tracks must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`) with DASH manifest. Stream configured as `test_streams_base_path + "MultiCodecStreams/stream_with_ac3_eac3.mpd"` in MediaValidationVariables.py | Verify multi-codec DASH stream accessible, both AC3 and EAC3 audio tracks present and parseable |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_ac3_eac3` configured in `MediaValidationVariables.py` with DASH manifest containing AC3 and EAC3 audio tracks | Verify `video_src_url_ac3_eac3` resolves to valid multi-codec stream with dual audio tracks |
| 4 | Device Configuration Parameters | Configuration parameters `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default 10 seconds per codec) must be retrievable from device configuration | Verify device config returns valid timeout  |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables, Wayland display active |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland configuration. Establish Wayland display session via RDKWindowManager. Initialize logging to `/opt/TDK/mediapipeline_test_step.log` | Verify environment variables load without errors, Wayland display active, logging initialized |
| 2 | Configure Test Parameters and Load Multi-Codec Stream | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` from device. Build `mediapipelinetests` command with test_name="test_playback_audio_change", stream_url=video_src_url_ac3_eac3, timeout=N | Verify device config retrieved successfully, command constructed with correct parameters |
| 3 | Create Playbin Pipeline and Load Multi-Codec Stream | Create `playbin` element via . Set `uri` property to multi-codec DASH stream URL via . Trigger state transitions to  via  | Verify playbin created, URI configured to multi-codec DASH stream, pipeline transitions to PLAYING |
| 4 | Retrieve and Verify Multiple Audio Tracks | Query playbin to determine number of audio streams via . Verify n-audio >= 2 (confirming AC3 and EAC3 tracks present). Query current audio index via  to identify default (AC3) track | Verify n-audio returns at least 2, current-audio successfully retrieved (typically 0 for first codec) |
| 5 | Verify Initial AC3 Audio Playback and Retrieve Audio-Tags | Emit "get-audio-tags" signal for default audio track via . Parse tag list using  to identify codec name (AC3). Log audio-tags including codec type, sample rate, channels as baseline. Poll playback position for 5-10 seconds to verify AC3 audio plays without interruption | Verify audio-tags successfully retrieved showing AC3 codec (e.g., audio/x-ac3), playback position advances linearly, no audio glitches or stalls |
| 6 | Switch to EAC3 Codec using current-audio and Flush Pipeline | Set `current-audio` property via  to switch to EAC3 track (index 1). Verify switch succeeded via  confirming value equals 1. Query current position via . Flush pipeline via  to clear buffered AC3 data. Wait 2 seconds for buffer refill with EAC3. Reset audio underflow flag | Verify current-audio property set to 1, position query succeeds, seek-flush executes successfully, 2-second wait completes, underflow flag reset |
| 7 | Verify Second EAC3 Audio Playback and Retrieve Audio-Tags | After seek-flush completes, playback continues with EAC3 codec now active. Emit "get-audio-tags" signal for EAC3 track via . Parse tag list using  to identify codec name (EAC3). Log audio-tags including codec type, sample rate, channels. Compare logged tags from Step 5 (AC3) with current tags (EAC3) to confirm different codec | Verify audio-tags successfully retrieved showing EAC3 codec (e.g., audio/x-eac3, different from AC3), codec change confirmed through tag comparison |
| 8 | Monitor EAC3 Playback Progress and Validate Continuity |  Verify position advances linearly from seek-flush point with no backward jumps. Monitor bus for `pts-error-callback` signals (should be none). Check for audio underflow conditions (should be none). Verify video playback continues uninterrupted during audio codec switch | Verify EAC3 position advances smoothly, no pts-error or underflow signals, video continues playing, audio output clear and artifact-free |
| 9 | Validate Dual Audio Codec Support and Release Resources | Review logged audio-tags from both codec playbacks. Verify codec identity confirmed via tags: Step 5 shows AC3, Step 7 shows EAC3 (distinctly different). Verify test framework output shows `Failures: 0`, `Errors: 0`. Set pipeline to  via . Call  to release all resources. Free allocated memory and close logging file | Verify audio-tags logs confirm both codecs properly identified, test completed successfully with zero failures/errors, pipeline reaches NULL state, all GStreamer resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
