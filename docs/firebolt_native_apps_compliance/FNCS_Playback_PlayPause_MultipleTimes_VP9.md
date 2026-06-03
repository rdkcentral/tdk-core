# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_182**

## TestCase Name
**FNCS_Playback_PlayPause_MultipleTimes_VP9**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that VP9 video stream supports multiple sequential play and pause operations over stressed iterations, ensuring proper playback state transitions and smooth resumption across repeated play/pause cycles.

**VIDEO CODEC:** VP9

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | VP9 stream (TDK_Asset_VP9_Stream.dash or WebM) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for each play or pause operation. Default value is 10 seconds |
| 5 | FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT configuration variable specifies the number of play/pause iterations to perform. Default value is 3 |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Multiple Play/Pause Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT configuration values from Device config file. Retrieve VP9 stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_trickplay operation specifying multiple play and pause operations. Execute command: `tdk_mediapipelinetests_trickplay https://<server_hosting_stream>:<port_number>/TDK_Asset_VP9_Stream.dash checkavstatus=<yes/no> operations=play:10,pause:5,play:10,pause:5,play:10,pause:5` (or per configured repeat count) | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with play/pause operations. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins VP9 stream playback using GStreamer playbin element with westeros-sink for rendering | VP9 stream playback must begin successfully without pipeline errors |
| 4 | Execute First Play Operation | Transition playbin to PLAYING state for the first time. Monitor playback for the configured timeout duration (default 10 seconds). Verify video frames render smoothly during this play period | Playback must transition to PLAYING state successfully. Video frames must render continuously without interruption |
| 5 | Execute First Pause Operation | Transition playbin to PAUSED state after first play. Verify that playback stops and pipeline transitions to PAUSED state. Monitor pause duration (default 5 seconds) | Pipeline must transition to PAUSED state successfully. Playback must stop smoothly |
| 6 | Execute Second Play Operation | Resume playback from paused position by transitioning to PLAYING state. Monitor playback for the configured timeout duration (default 10 seconds). Verify smooth resumption and continued frame rendering | Playback must resume successfully from paused position. Video frames must render continuously without interruption |
| 7 | Execute Second Pause Operation | Transition playbin back to PAUSED state. Verify that playback stops cleanly and pipeline remains in PAUSED state. Monitor pause duration (default 5 seconds) | Pipeline must transition to PAUSED state successfully. Playback must stop smoothly |
| 8 | Execute Third Play Operation | Resume playback again from current paused position. Monitor playback for the configured timeout duration (default 10 seconds). Verify smooth resumption and continued frame rendering | Playback must resume successfully. Video frames must render continuously without interruption |
| 9 | Execute Third Pause Operation | Transition playbin to PAUSED state for final time. Verify clean state transition and pause operation completion. Monitor pause duration (default 5 seconds) | Pipeline must transition to PAUSED state successfully. Final pause operation must complete without errors |
| 10 | Monitor Overall Playback Quality | Throughout all play/pause iterations, monitor video frame rendering using westerossink "stats" property. Verify that video frame drop rate does not exceed 1% across all state transitions. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder remains active | Video frames must render with drop rate below 1%. All state transitions must occur without pipeline errors. If AV status check is enabled, video decoder must show continuous activity |
| 11 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify all play/pause iterations completed successfully | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". All play/pause operations must be confirmed as successful |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 4 minutes

**Priority:** High

**Release Version:** M121
