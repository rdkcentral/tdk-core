# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_192**

## TestCase Name
**FNCS_Playback_Duration_Test_DASH**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate accurate retrieval and verification of playback duration for DASH adaptive streaming content through the GStreamer media pipeline.

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | DASH stream (TDK_Asset_DASH_Stream.mpd) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the timeout in seconds for duration verification. Default value is "10" |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Duration Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve DASH stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_playback_duration operation. Execute command: `tdk_mediapipelinetests_duration https://<server_hosting_stream>:<port_number>/TDK_Asset_DASH_Stream.mpd checkavstatus=<yes/no> timeout=<seconds>` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly. Test application must start execution without errors |
| 3 | Initialize GStreamer Pipeline | Create and configure GStreamer playbin element for DASH stream playback with westerossink for video rendering | GStreamer pipeline must initialize successfully with DASH container parser and codec plugins detected |
| 4 | Begin Playback and Duration Monitoring | Start playback of DASH stream and begin monitoring total duration. The test plays the stream for the configured timeout duration (default 10 seconds) while tracking playback position | Stream playback must begin successfully. Playback must continue for the specified duration without errors or pipeline failures |
| 5 | Retrieve and Verify Stream Duration | Query GStreamer pipeline for total stream duration property. Compare retrieved duration against expected 9-second verification threshold | Retrieved duration value must be obtained from GStreamer without errors. Duration must be valid and retrievable |
| 6 | Monitor Playback Quality During Duration Test | Throughout playback, monitor video frame rendering using westerossink "stats" property. Verify that video frame drop rate does not exceed 1%. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder remains active | Video frames must render with drop rate below 1%. Frame rendering must be continuous throughout the duration test. If AV status check is enabled, video decoder must show continuous activity |
| 7 | Validate Duration Test Results | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify that duration retrieval completed successfully and stream duration was properly verified | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Duration test must be confirmed as successful |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
