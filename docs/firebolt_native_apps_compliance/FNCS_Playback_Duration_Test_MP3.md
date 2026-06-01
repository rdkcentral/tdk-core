# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_215**

## TestCase Name
**FNCS_Playback_Duration_Test_MP3**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate accurate retrieval and verification of playback duration for MP3 audio-only content through the GStreamer media pipeline.

**AUDIO CODEC:** MP3

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | MP3 audio stream (TDK_Asset_MP3_Stream.mp3) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level audio playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the timeout in seconds for duration verification. Default value is "10" |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for audio playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present (though not required for audio-only tests). Initialize audio output interface without requiring display rendering | All environment variables must be set successfully and audio interface must be ready for playback |
| 2 | Configure and Execute Duration Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve MP3 audio stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_audio_duration operation. Execute command: `tdk_mediapipelinetests_duration https://<server_hosting_stream>:<port_number>/TDK_Asset_MP3_Stream.mp3 checkavstatus=<yes/no> timeout=<seconds>` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly. Test application must start execution without errors |
| 3 | Initialize GStreamer Pipeline | Create and configure GStreamer playbin element for MP3 audio-only playback. Initialize MP3 audio decoder and configure native audio-sink for audio output. Verify that MP3 audio stream is properly recognized without video sink initialization | GStreamer pipeline must initialize successfully with MP3 audio decoder. Audio-only pipeline must be properly configured without video rendering components |
| 4 | Begin Audio Playback and Duration Monitoring | Start playback of MP3 audio stream and begin monitoring total duration. The test plays the audio for the configured timeout duration (default 10 seconds) while tracking audio playback position | Audio playback must begin successfully. Audio must render continuously for the specified duration without errors or pipeline failures. MP3 frames must be properly decoded |
| 5 | Retrieve and Verify Stream Duration | Query GStreamer pipeline for total stream duration property. Compare retrieved duration against expected 9-second verification threshold | Retrieved duration value must be obtained from GStreamer without errors. Duration must be valid and retrievable for audio-only content |
| 6 | Monitor Audio Playback Quality During Duration Test | Throughout playback, monitor audio frame rendering using native audio-sink "stats" property. Verify that audio frame drop rate does not exceed 1% and audio output is continuous without distortion | Audio frames must render with drop rate below 1%. Audio rendering must be continuous throughout the duration test. Audio output quality must be maintained |
| 7 | Validate Duration Test Results | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify that duration retrieval completed successfully for MP3 audio stream | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Duration test must be confirmed as successful |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
