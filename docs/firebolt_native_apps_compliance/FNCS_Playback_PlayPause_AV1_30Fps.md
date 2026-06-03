# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_325**

## TestCase Name
**FNCS_Playback_PlayPause_AV1_30Fps**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that DASH adaptive streaming with AV1 video codec at 30 frames per second supports stable play and pause operations, ensuring smooth state transitions and proper resumption of playback across multiple cycles.

**VIDEO CODEC:** AV1

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | AV1 DASH stream (TDK_Asset_AV1_DASH_Stream.mpd) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the timeout in seconds for video playback verification. Default value is "10" |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Play-Pause Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve AV1 DASH stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_playback_fps operation. Execute command: `tdk_mediapipelinetests_playback https://<server_hosting_stream>:<port_number>/TDK_Asset_AV1_DASH_Stream.mpd checkavstatus=<yes/no> timeout=<seconds>` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins DASH stream playback with AV1 codec at 30 fps using GStreamer playbin element. Confirm that AV1 video decoder initializes properly and begins rendering frames at the correct frame rate | DASH stream playback must begin successfully without pipeline errors. AV1 video decoder must initialize and render at 30 fps frame rate |
| 4 | Transition to Play State | Verify that playbin state transitions to PLAYING and video frames render smoothly with AV1 codec. Monitor frame rendering and ensure consistent playback at 30 fps throughout the operation | Playbin must transition to PLAYING state successfully. Video frames must render continuously at consistent 30 fps without interruption |
| 5 | Execute Pause Operation | Transition playbin to PAUSED state during playback. Verify that the pipeline pauses cleanly and maintains the current position in the stream. Confirm that video and audio rendering stops | Pipeline must transition to PAUSED state successfully. Playback must stop cleanly at current position |
| 6 | Execute Resume Play Operation | Resume playback by transitioning playbin back to PLAYING state after pause. Verify that playback resumes from paused position with smooth frame rendering continuing at 30 fps | Playbin must transition to PLAYING state successfully. Video frames must resume rendering from paused position at 30 fps without interruption |
| 7 | Monitor Overall Playback Quality | Throughout play and pause operations, monitor video frame rendering using westerossink "stats" property. Verify that video frame drop rate does not exceed 1% during playback. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder remains active during all play-pause cycles | Video frames must render with drop rate below 1%. All state transitions must occur without pipeline errors. If AV status check is enabled, video decoder must show continuous activity |
| 8 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify all play-pause operations completed successfully | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". All play-pause operations must be confirmed as successful |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 1-2 minutes

**Priority:** High

**Release Version:** M134
