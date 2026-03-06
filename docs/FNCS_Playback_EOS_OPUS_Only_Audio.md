# FNCS_Playback_EOS_OPUS_Only_Audio Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_315

## TestCase Name
FNCS_Playback_EOS_OPUS_Only_Audio

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To test the End Of Stream (EOS) detection scenario for an audio-only OPUS stream through 'playbin' and 'westerossink' GStreamer elements, validating the media pipeline's capability to properly detect stream completion and handle EOS events for audio-only content without video components.

**AUDIO CODEC:** OPUS

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | OPUS audio-only stream must be available and referenced in MediaValidationVariables.audio_src_url_short_duration_webm_opus (TDK_Asset_OPUS_Audio_only_15sec.webm) |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 4 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 5 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_USE_VIDEO_SINK configuration in Video_Accelerator.config specifies custom video sink element, currently empty (uses default) |
| 7 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 8 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 10 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 11 | FIREBOLT_COMPLIANCE_EOS_TIMEOUT configuration in Video_Accelerator.config specifies EOS detection timeout in seconds (default 6 minutes for test application) |
| 12 | audio_src_url_short_duration_webm_opus variable in MediaValidationVariables.py contains short-duration OPUS audio stream URL (TDK_Asset_OPUS_Audio_only_15sec.webm) for EOS testing |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env and create display for playback environment using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_EOS_TIMEOUT config values, get OPUS audio stream URL from MediaValidationVariables.audio_src_url_short_duration_webm_opus, construct tdk_mediapipelinetests command with only_audio flag, and run test_EOS with OPUS stream | Configuration values retrieved, OPUS audio stream URL obtained, command executed: `tdk_mediapipelinetests test_EOS <OPUS_AUDIO_STREAM_URL> checkavstatus=no timeout=<EOS_TIMEOUT> only_audio`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element and configure for audio-only OPUS stream playback, disable video components and enable audio-only mode with westerossink | Playbin element created successfully with OPUS audio-only stream support and video components disabled |
| 4 | Configure Audio-Only Output | Create and configure audio sink element for OPUS audio-only playback, establish audio processing without video pipeline components | Audio sink element configured successfully for OPUS audio-only playback with proper audio routing |
| 5 | Enable EOS Detection | Configure pipeline to monitor for End-of-Stream events from OPUS audio decoder, set up EOS message handling and timeout mechanism | EOS detection enabled successfully with proper message handling and timeout configuration |
| 6 | Start OPUS Audio-Only Playback | Set pipeline to PLAYING state and begin playback with OPUS audio-only codec, monitor for audio frames and EOS events | Pipeline transitions to PLAYING state successfully, OPUS audio-only playback starts, and EOS monitoring activated |
| 7 | Monitor Stream Completion | Continuously monitor OPUS audio-only playback until natural stream completion or EOS timeout, verify audio frame processing and stream position | OPUS audio-only playback proceeds successfully with continuous audio frame processing and proper stream position tracking |
| 8 | Detect EOS Event | Wait for End-of-Stream message from OPUS audio decoder when stream reaches natural completion, verify EOS signal reception within configured timeout | EOS message received successfully from OPUS audio decoder when stream completes naturally within timeout period |
| 9 | Validate EOS Handling | Verify proper EOS event processing and pipeline state transition after stream completion, ensure clean shutdown of audio-only components | EOS event processed correctly with proper pipeline state transitions and clean audio component shutdown |
| 10 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating OPUS audio-only EOS detection completed without errors |
| 11 | Cleanup Pipeline | Set playbin pipeline to NULL state, release OPUS audio resources, and clean up audio-only components | Pipeline transitions to NULL state successfully, OPUS audio resources released, and audio-only components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M132