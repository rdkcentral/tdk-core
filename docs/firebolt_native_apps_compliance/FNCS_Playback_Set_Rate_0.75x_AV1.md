# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_83**

## TestCase Name
**FNCS_Playback_Set_Rate_0.75x_AV1**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that an AV1 stream can be played back at a reduced playback rate of 0.75x (three-quarters speed), ensuring smooth slow-motion playback and proper rate transitions.

**VIDEO CODEC:** AV1

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | AV1 stream (TDK_Asset_AV1_Stream.mpd) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for which the slow motion operation should be carried out. Default value is 10 seconds |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Slow Motion Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve AV1 stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_trickplay operation and slowMotion0.75x rate parameter. Execute command: `tdk_mediapipelinetests_trickplay https://<server_hosting_stream>:<port_number>/TDK_Asset_AV1_Stream.mpd checkavstatus=<yes/no> operations=slowMotion0.75x:<timeout>` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly. Test application must start execution without errors |
| 3 | Verify Playback Starts | Validate that the mediapipeline initializes and begins AV1 stream playback using GStreamer playbin element with westeros-sink for rendering | AV1 stream playback must begin successfully without pipeline errors |
| 4 | Apply Slow Motion Rate Transition | Execute the slowMotion0.75x operation which reduces the playback rate to 75% of normal speed (0.75x rate) | Playback rate must transition to 0.75x successfully, and media continues playing at reduced speed |
| 5 | Monitor Slow Motion Playback | Monitor playback position progression during slow motion operation for the configured timeout duration (default 10 seconds). Verify playback position increments occur at 0.75x rate intervals. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder status | Playback position must progress at 0.75x rate smoothly. If AV status check is enabled, video decoder must show active decoding without interruptions |
| 6 | Verify Playback Quality During Slow Motion | Verify that video frames are rendered correctly during slow motion using westerossink "stats" property to monitor frames rendered and dropped. Monitor that frame drop rate does not exceed 1% during the slow motion operation | Video frames must render continuously with frame drop rate less than 1% |
| 7 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify pipeline closes cleanly after slow motion timeout expires | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Pipeline must close gracefully without errors |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M121
