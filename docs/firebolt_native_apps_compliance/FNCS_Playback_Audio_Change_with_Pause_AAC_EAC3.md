# FNCS_Playback_Audio_Change_with_Pause_AAC_EAC3 Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_129

## TestCase Name
FNCS_Playback_Audio_Change_with_Pause_AAC_EAC3

## Table Of Contents
- [FNCS\_Playback\_Audio\_Change\_with\_Pause\_AAC\_EAC3 Test Case Documentation](#fncs_playback_audio_change_with_pause_aac_eac3-test-case-documentation)
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Table Of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To verify the media pipeline's capability to switch between different audio codecs (AAC and EAC3) present in the same stream without changing the video, while incorporating pause/resume functionality to test codec switching resilience during playback state transitions. This test validates dynamic audio codec switching functionality combined with playback control operations by monitoring playback continuity and verifying successful codec detection during runtime transitions with pause operations.

**AUDIO CODECS:** AAC ⟷ EAC3 **WITH PAUSE/RESUME TESTING**

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | Multi-codec stream with AAC and EAC3 audio tracks must be available and referenced in MediaValidationVariables.video_src_url_aac_eac3 |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 4 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 5 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_USE_VIDEO_SINK configuration in Video_Accelerator.config specifies custom video sink element, currently empty (uses default) |
| 7 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 8 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 10 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 11 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration in Video_Accelerator.config specifies playback duration per codec in seconds, default 10 seconds |
| 12 | FIREBOLT_COMPLIANCE_PLAYBACK_LATENCY_THRESHOLD configuration in Video_Accelerator.config specifies acceptable playback latency threshold in milliseconds |
| 13 | video_src_url_aac_eac3 variable in MediaValidationVariables.py contains multi-codec stream URL (TDK_Asset_Sunrise_AAC_EAC3_v2.mp4) with both AAC and EAC3 audio tracks |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT config values, get multi-codec stream URL from MediaValidationVariables.video_src_url_aac_eac3, construct tdk_mediapipelinetests command with timeout parameter, and run test_audio_change_with_pause with AAC/EAC3 stream | Configuration values retrieved, multi-codec stream URL obtained, command executed: `tdk_mediapipelinetests test_audio_change_with_pause <AAC_EAC3_STREAM_URL> checkavstatus=no timeout=10`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element and configure with multi-codec audio stream support, enable audio codec switching capability using current-audio property with pause/resume functionality | Playbin element created successfully with multi-codec audio stream support, codec switching capability enabled, and pause/resume controls configured |
| 4 | Configure Audio Output | Create and configure audio sink element for multi-codec audio playback, establish audio codec detection monitoring with pause state handling | Audio sink element configured successfully for multi-codec playback with codec detection monitoring and pause state management enabled |
| 5 | Start Initial AAC Playback | Set pipeline to PLAYING state and begin playback with initial AAC audio codec, monitor audio frames and codec detection | Pipeline transitions to PLAYING state successfully, AAC audio playback starts, and codec detection confirms AAC audio stream |
| 6 | Validate AAC Playback Phase | Monitor AAC audio playback for configured timeout duration (default 10 seconds), verify audio frames and codec stability | AAC audio playback proceeds successfully for full timeout duration with stable audio frames and confirmed AAC codec detection |
| 7 | Execute Pause Operation | Pause the playback pipeline using GStreamer state management, verify pipeline transitions to PAUSED state successfully | Pipeline pauses successfully, audio and video output stops, and pipeline state confirmed as PAUSED |
| 8 | Initiate Audio Codec Switch During Pause | Use playbin current-audio property to switch from AAC to EAC3 audio track while pipeline is in PAUSED state, maintaining video track continuity | Audio codec switch initiated successfully during pause state using current-audio property, video track remains unchanged |
| 9 | Resume Playback with EAC3 | Resume playback by transitioning pipeline from PAUSED to PLAYING state, verify EAC3 audio codec activation and seamless playback continuation | Pipeline resumes successfully to PLAYING state, EAC3 audio playback starts, and codec transition completed without artifacts |
| 10 | Validate EAC3 Playback Phase | Monitor EAC3 audio playback for configured timeout duration (default 10 seconds), verify audio frames and codec stability after pause/resume cycle | EAC3 audio playback proceeds successfully for full timeout duration with stable audio frames and confirmed EAC3 codec detection |
| 11 | Verify Codec Detection | Check output for AAC and EAC3 codec detection confirmations using checkifCodecPlayed validation for both audio codecs across pause/resume operations | Output contains successful codec detection for both "aac" and "e-ac-3" codecs indicating proper codec recognition through pause/resume cycle |
| 12 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating AAC to EAC3 audio codec switching with pause/resume completed without errors |
| 13 | Cleanup Pipeline | Set playbin pipeline to NULL state, release multi-codec audio resources, and clean up codec switching and pause/resume components | Pipeline transitions to NULL state successfully, multi-codec audio resources released, and all pause/resume components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121