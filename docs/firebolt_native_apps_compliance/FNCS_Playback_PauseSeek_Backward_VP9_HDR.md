# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_379**

## TestCase Name
**FNCS_Playback_PauseSeek_Backward_VP9_HDR**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that DASH stream playback with VP9 video codec in HDR (High Dynamic Range) format supports backward seek operations after pause, ensuring proper playback state transitions from paused state to the beginning position and resumption of playback with HDR content.

**VIDEO CODEC:** VP9 (HDR)

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | VP9 HDR DASH stream (TDK_Asset_VP9_HDR_DASH_Stream.mpd) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for playback operations. Default value is 10 seconds |
| 5 | FIREBOLT_COMPLIANCE_SEEK_POSITION configuration variable specifies the target position in seconds for backward seek operation. Default value is 0 seconds (beginning of stream) |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Pause-Seek-Play Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_SEEK_POSITION configuration values from Device config file. Retrieve VP9 HDR DASH stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_trickplay operation specifying pause, backward seek, and play operations. Execute command: `tdk_mediapipelinetests_trickplay https://<server_hosting_stream>:<port_number>/TDK_Asset_VP9_HDR_DASH_Stream.mpd checkavstatus=<yes/no> operations=pause:5,seek:0,play:10` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with pause, seek, and play operations. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins VP9 HDR DASH stream playback using GStreamer playbin element with westeros-sink for rendering | VP9 HDR DASH stream playback must begin successfully without pipeline errors |
| 4 | Execute Pause Operation | Transition playbin to PAUSED state. Verify that playback stops and pipeline transitions to PAUSED state. Monitor pause duration (5 seconds) | Pipeline must transition to PAUSED state successfully. Playback must stop smoothly |
| 5 | Execute Backward Seek Operation | From the paused state, execute backward seek to position 0 (beginning of stream). Verify that seek operation completes and pipeline remains in valid state without errors | Seek operation must complete successfully. Pipeline must transition to seek target position. Playback position must update to approximately 0 seconds |
| 6 | Resume Playback After Seek | Transition playbin from paused state to PLAYING state after seek completion. Monitor playback for the configured timeout duration (default 10 seconds). Verify video frames render smoothly from the beginning with HDR content | Playback must resume successfully from the beginning. Video frames must render continuously without interruption. HDR tone mapping must be maintained |
| 7 | Monitor Overall Playback Quality | Throughout pause, seek, and play operations, monitor video frame rendering using westerossink "stats" property. Verify that video frame drop rate does not exceed 1% across all state transitions. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder remains active | Video frames must render with drop rate below 1%. All state transitions must occur without pipeline errors. If AV status check is enabled, video decoder must show continuous activity |
| 8 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify pause, seek, and play operations completed successfully | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". All trickplay operations must be confirmed as successful |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M136
