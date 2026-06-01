# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_375**

## TestCase Name
**FNCS_Playback_Duration_Test_VP9_HDR**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate accurate retrieval and verification of playback duration for WebM container format with VP9 HDR video codec and Opus audio codec through the GStreamer media pipeline with High Dynamic Range rendering support.

**VIDEO CODEC:** VP9 (HDR)

**AUDIO CODEC:** Opus

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | VP9 HDR WebM stream (TDK_Asset_VP9_HDR_Stream.webm) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the timeout in seconds for duration verification. Default value is "10" |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command. Verify that display supports HDR rendering capabilities | All environment variables must be set successfully and display for playback must be created successfully with HDR support verified using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Duration Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve VP9 HDR WebM stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_playback_duration operation. Execute command: `tdk_mediapipelinetests_duration https://<server_hosting_stream>:<port_number>/TDK_Asset_VP9_HDR_Stream.webm checkavstatus=<yes/no> timeout=<seconds>` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly. Test application must start execution without errors |
| 3 | Initialize GStreamer Pipeline | Create and configure GStreamer playbin element for HDR WebM container playback. Initialize VP9 HDR video decoder with HDR metadata processing. Initialize Opus audio decoder. Configure westerossink for HDR video rendering with HDR tone mapping. Verify that WebM container parser properly handles VP9 HDR metadata (BT.2100, HDR10, or similar) | GStreamer pipeline must initialize successfully with HDR-aware WebM parser. VP9 HDR and Opus decoders must initialize properly. HDR metadata must be properly detected |
| 4 | Begin Playback and Duration Monitoring | Start playback of VP9 HDR stream and begin monitoring total duration. The test plays the stream for the configured timeout duration (default 10 seconds) while tracking playback position and HDR metadata processing | Stream playback must begin successfully with HDR tone mapping applied. Video and audio must render continuously for the specified duration without errors. HDR metadata must be properly processed |
| 5 | Retrieve and Verify Stream Duration | Query GStreamer pipeline for total stream duration property from WebM container metadata. Compare retrieved duration against expected 9-second verification threshold | Retrieved duration value must be obtained from GStreamer without errors. Duration must be accurately extracted from HDR-encoded WebM container metadata |
| 6 | Monitor Playback Quality During Duration Test | Throughout playback, monitor video frame rendering using westerossink "stats" property with HDR tone mapping active. Verify that video frame drop rate does not exceed 1% despite HDR processing overhead. Monitor audio rendering using native audio-sink "stats" property. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level VP9 HDR decoder remains active | Video frames must render with drop rate below 1% under HDR processing. Audio frames must render with drop rate below 1%. All streams must render continuously throughout duration test with HDR enhancements applied. If AV status check is enabled, VP9 HDR decoder activity must be continuous |
| 7 | Validate Duration Test Results | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify that duration retrieval completed successfully for VP9 HDR WebM container format with proper HDR metadata processing | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Duration test must be confirmed as successful with HDR support validated |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M136
