# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_176**

## TestCase Name
**FNCS_Playback_PlayPause_ExtendedDuration_HLS**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that HLS adaptive streaming with H264 video codec supports extended duration play and pause operations, ensuring stable playback state transitions and resumption across multiple prolonged playback cycles with adaptive bitrate management.

**VIDEO CODEC:** H264

**AUDIO CODEC:** AAC

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | HLS stream (TDK_Asset_HLS_Stream.m3u8) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_EXTENDEDDURATION_TIMEOUT configuration variable specifies the duration in seconds for each extended play or pause operation. Default value is 10 seconds |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Extended Duration Play-Pause Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_EXTENDEDDURATION_TIMEOUT configuration values from Device config file. Retrieve HLS stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_trickplay operation specifying extended duration play and pause operations for adaptive streaming. Execute command: `tdk_mediapipelinetests_trickplay https://<server_hosting_stream>:<port_number>/TDK_Asset_HLS_Stream.m3u8 checkavstatus=<yes/no> operations=play:<timeout>,pause:<timeout>,play:5` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with extended duration play/pause operations. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins HLS stream playback using GStreamer playbin element with westeros-sink for rendering. Confirm adaptive stream is detected and playback begins at appropriate bitrate | HLS stream playback must begin successfully without pipeline errors. Adaptive stream detection must be successful |
| 4 | Execute Extended Play Operation | Transition playbin to PLAYING state and maintain playback for the extended duration timeout (default 10 seconds). Monitor playback continuously during this prolonged period while allowing adaptive bitrate transitions to occur naturally. Verify that video frames render smoothly throughout the extended play duration | Playback must transition to PLAYING state successfully. Video must continue rendering smoothly for the entire extended duration. Adaptive bitrate transitions must occur without disruption |
| 5 | Execute Pause Operation | Transition playbin to PAUSED state after extended play. Verify that playback stops cleanly and pipeline transitions to PAUSED state. Monitor pause duration (timeout period) | Pipeline must transition to PAUSED state successfully. Playback must stop smoothly and remain paused for the configured duration |
| 6 | Resume Extended Play Operation | Resume playback by transitioning playbin back to PLAYING state. Maintain playback for the extended duration timeout (default 10 seconds). Monitor for adaptive bitrate adjustments during resumption. Verify smooth resumption and continuous frame rendering | Playback must resume successfully from paused position. Video frames must render smoothly for the entire extended duration. Adaptive bitrate re-stabilization must occur without disruption |
| 7 | Execute Final Play Operation | Perform final brief play operation (5 seconds) to verify playback stability. Confirm video frames continue to render without issues | Final playback phase must complete successfully. Video frames must render continuously |
| 8 | Monitor Overall Playback Quality | Throughout all extended play and pause operations, monitor video frame rendering using westerossink "stats" property. Verify that video frame drop rate does not exceed 1% across all extended periods, state transitions, and adaptive bitrate changes. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder remains active | Video frames must render with drop rate below 1%. All state transitions and bitrate changes must occur without pipeline errors. If AV status check is enabled, video decoder must show continuous activity |
| 9 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify all extended play/pause operations completed successfully | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". All extended duration operations must be confirmed as successful |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3-5 minutes

**Priority:** High

**Release Version:** M121
