# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_292**

## TestCase Name
**FNCS_Playback_Duration_Test_4K_VP9**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate accurate retrieval and verification of playback duration for 4K resolution WebM container format with VP9 video codec and Opus audio codec through the GStreamer media pipeline.

**VIDEO CODEC:** VP9

**AUDIO CODEC:** Opus

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | 4K VP9 WebM stream (TDK_Asset_4K_VP9_Stream.webm) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the timeout in seconds for duration verification. Default value is "10" |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command. Verify that display supports 4K resolution (3840x2160 or equivalent) | All environment variables must be set successfully and display for playback must be created successfully with 4K capability verified using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Duration Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve 4K VP9 WebM stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_playback_duration operation and set checkAudioFPS=no. Execute command: `tdk_mediapipelinetests_duration https://<server_hosting_stream>:<port_number>/TDK_Asset_4K_VP9_Stream.webm checkavstatus=<yes/no> timeout=<seconds> checkAudioFPS=no` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with audio FPS validation disabled. Test application must start execution without errors |
| 3 | Initialize GStreamer Pipeline | Create and configure GStreamer playbin element for 4K WebM container playback. Initialize VP9 video decoder for 4K content and Opus audio decoder. Configure westerossink for 4K video rendering and native audio-sink for audio output. Verify that WebM container parser is properly initialized for complex audio formats | GStreamer pipeline must initialize successfully with WebM container parser. VP9 and Opus decoders must initialize properly for 4K WebM format |
| 4 | Begin Playback and Duration Monitoring | Start playback of 4K VP9 stream and begin monitoring total duration. The test plays the stream for the configured timeout duration (default 10 seconds) while tracking playback position. Verify that 4K resolution is maintained throughout playback | Stream playback must begin successfully at 4K resolution. Video and audio must render continuously for the specified duration without errors or resolution downscaling. WebM container must be properly parsed |
| 5 | Retrieve and Verify Stream Duration | Query GStreamer pipeline for total stream duration property from WebM container metadata. Compare retrieved duration against expected 9-second verification threshold for 4K content | Retrieved duration value must be obtained from GStreamer without errors. Duration must be accurately extracted from WebM container metadata |
| 6 | Monitor Playback Quality During Duration Test | Throughout playback, monitor 4K video frame rendering using westerossink "stats" property. Verify that video frame drop rate does not exceed 1% at 4K resolution. Audio FPS validation is disabled for complex WebM audio formats (Opus). If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder remains active for 4K VP9 decoding | 4K video frames must render with drop rate below 1%. 4K resolution must be maintained throughout. Audio FPS monitoring must be disabled as configured. If AV status check is enabled, 4K video decoder activity must be continuous |
| 7 | Validate Duration Test Results | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify that duration retrieval completed successfully for 4K VP9 WebM container format | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Duration test must be confirmed as successful |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M130
