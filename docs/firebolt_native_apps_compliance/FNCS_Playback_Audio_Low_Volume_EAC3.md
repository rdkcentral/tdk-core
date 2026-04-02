# FNCS_Playback_Audio_Low_Volume_EAC3 Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_136

## TestCase Name
FNCS_Playback_Audio_Low_Volume_EAC3

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To verify whether audio is playing at a specified low volume level using EAC3 stream, validating the media pipeline's capability to handle volume control operations and maintain audio playback quality at reduced volume settings. This test ensures proper audio volume management functionality by monitoring playback performance and verifying successful audio delivery at controlled volume levels.

**AUDIO CODEC:** EAC3

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | EAC3 audio stream must be available and referenced in MediaValidationVariables.video_src_url_ec3 |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 4 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 5 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_USE_VIDEO_SINK configuration in Video_Accelerator.config specifies custom video sink element, currently empty (uses default) |
| 7 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 8 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 10 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 11 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration in Video_Accelerator.config specifies playback duration in seconds, default 10 seconds |
| 12 | video_src_url_ec3 variable in MediaValidationVariables.py contains EAC3 stream URL (atfms_291_dash_tdk_avc_eac3_fmp4.mpd) for volume testing |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env and create display for playback environment using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT config values, get EAC3 stream URL from MediaValidationVariables.video_src_url_ec3, construct tdk_mediapipelinetests command with volume parameter (0.5), and run test_audio_volume with EAC3 stream | Configuration values retrieved, EAC3 stream URL obtained, command executed: `tdk_mediapipelinetests test_audio_volume <EAC3_STREAM_URL> checkavstatus=no timeout=10 volume_set=0.5`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element and configure with EAC3 audio stream support, enable volume control capability using GStreamer volume element | Playbin element created successfully with EAC3 audio stream support and volume control capability enabled |
| 4 | Configure Audio Output | Create and configure audio sink element for EAC3 audio playback with volume control, establish audio level monitoring | Audio sink element configured successfully for EAC3 playback with volume control and audio level monitoring enabled |
| 5 | Set Low Volume Level | Configure audio volume to low setting (0.5 or 50%) using GStreamer volume property before starting playback | Volume level set successfully to 0.5 (50% of maximum volume) and volume control confirmed |
| 6 | Start EAC3 Playback with Volume Control | Set pipeline to PLAYING state and begin playback with EAC3 audio codec at specified low volume level, monitor audio frames and volume compliance | Pipeline transitions to PLAYING state successfully, EAC3 audio playback starts at low volume level, and volume setting confirmed |
| 7 | Validate Low Volume EAC3 Playback | Monitor EAC3 audio playback at low volume for configured timeout duration (default 10 seconds), verify audio frames and volume level stability | EAC3 audio playback proceeds successfully for full timeout duration with stable audio frames at consistent low volume level |
| 8 | Execute Pause Operation | Pause the playback pipeline for 5 seconds using GStreamer state management, verify volume level is maintained during pause | Pipeline pauses successfully for 5 seconds, audio output stops, and volume setting preserved during pause state |
| 9 | Resume Volume-Controlled Playback | Resume playback by transitioning pipeline from PAUSED to PLAYING state, verify volume level is maintained after resume | Pipeline resumes successfully to PLAYING state, EAC3 audio playback continues at same low volume level without volume drift |
| 10 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating EAC3 audio playback with volume control completed without errors |
| 11 | Cleanup Pipeline | Set playbin pipeline to NULL state, release EAC3 audio resources, and clean up volume control components | Pipeline transitions to NULL state successfully, EAC3 audio resources released, and volume control components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121