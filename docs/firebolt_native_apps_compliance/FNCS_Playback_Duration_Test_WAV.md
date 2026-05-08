# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_228**

## TestCase Name
**FNCS_Playback_Duration_Test_WAV**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate accurate retrieval and verification of playback duration for WAV audio-only content with PCM audio codec through the GStreamer media pipeline.

**AUDIO CODEC:** PCM (Pulse Code Modulation)

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | WAV PCM audio stream (TDK_Asset_WAV_PCM_Stream.wav) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level audio playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the timeout in seconds for duration verification. Default value is "10" |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for audio playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present (though not required for audio-only tests). Initialize audio output interface without requiring display rendering. Verify that PCM audio support is available on the device | All environment variables must be set successfully and audio interface must be ready for PCM playback |
| 2 | Configure and Execute Duration Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve WAV PCM audio stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_audio_duration operation and set checkAudioFPS=no. Execute command: `tdk_mediapipelinetests_duration https://<server_hosting_stream>:<port_number>/TDK_Asset_WAV_PCM_Stream.wav checkavstatus=<yes/no> timeout=<seconds> checkAudioFPS=no` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with audio FPS validation disabled. Test application must start execution without errors |
| 3 | Initialize GStreamer Pipeline | Create and configure GStreamer playbin element for WAV PCM audio-only playback. Initialize PCM audio decoder and configure native audio-sink for audio output. Verify that WAV container parser is properly initialized. Audio FPS validation must be disabled for PCM format | GStreamer pipeline must initialize successfully with WAV parser and PCM audio decoder. Audio-only pipeline must be properly configured without video rendering components. Audio FPS monitoring must be disabled as specified |
| 4 | Begin Audio Playback and Duration Monitoring | Start playback of WAV PCM stream and begin monitoring total duration. The test plays the audio for the configured timeout duration (default 10 seconds) while tracking audio playback position | Audio playback must begin successfully. Audio must render continuously for the specified duration without errors or pipeline failures. PCM samples must be properly decoded |
| 5 | Retrieve and Verify Stream Duration | Query GStreamer pipeline for total stream duration property from WAV container metadata. Compare retrieved duration against expected 9-second verification threshold | Retrieved duration value must be obtained from GStreamer without errors. Duration must be valid and retrievable for PCM audio-only content |
| 6 | Monitor Audio Playback Quality During Duration Test | Throughout playback, monitor audio frame rendering using native audio-sink "stats" property. Audio FPS validation is disabled for PCM format. Verify that audio output is continuous without distortion or skipping. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level audio decoder remains active | Audio rendering must be continuous throughout the duration test without interruption. Audio output quality must be maintained. Audio FPS monitoring must be disabled as configured. If AV status check is enabled, audio decoder activity must be continuous |
| 7 | Validate Duration Test Results | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify that duration retrieval completed successfully for WAV PCM audio stream | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Duration test must be confirmed as successful |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
