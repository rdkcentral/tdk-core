# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_61**

## TestCase Name
**FNCS_Playback_PlaySeek_Forward_H264**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that an H264 stream supports forward seek operation during playback, ensuring proper seeking accuracy and smooth playback resumption at the target position.

**VIDEO CODEC:** H264

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | H264 DASH stream (TDK_Asset_H264_DASH_Stream.mpd) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for normal playback before seek operation. Default value is 10 seconds |
| 5 | FIREBOLT_COMPLIANCE_SEEK_POSITION configuration variable specifies the target position in seconds where the seek operation should be performed. Default value is 30 seconds |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Forward Seek Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_SEEK_POSITION configuration values from Device config file. Retrieve H264 DASH stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_playseek operation specifying forward seek operation. Execute command: `tdk_mediapipelinetests_playseek https://<server_hosting_stream>:<port_number>/TDK_Asset_H264_DASH_Stream.mpd checkavstatus=<yes/no> operations=seek:<seek_position>` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins H264 stream playback using GStreamer playbin element with westeros-sink for rendering | H264 stream playback must begin successfully without pipeline errors |
| 4 | Execute Forward Seek Operation | Perform a forward seek operation to the position specified by FIREBOLT_COMPLIANCE_SEEK_POSITION (default 30 seconds). Verify seek completion and confirm playback position is at the target seek location | Forward seek operation must complete successfully. Playback position must be at or near the specified seek position. No pipeline errors should occur |
| 5 | Verify Playback Resumption After Seek | Confirm that playback resumes smoothly at the new position after the seek operation completes | Media playback must continue seamlessly from the seek position without interruption or artifacts |
| 6 | Monitor Playback Quality After Seek | Monitor playback position progression and verify smooth playback. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder status is active | Playback must progress smoothly. If AV status check is enabled, video decoder must show active decoding without interruptions |
| 7 | Verify Video Frame Quality | Verify that video frames are rendered correctly after seek using westerossink "stats" property to monitor frames rendered and dropped. Monitor that frame drop rate does not exceed 1% | Video frames must render continuously with frame drop rate less than 1% |
| 8 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify pipeline closes cleanly | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Pipeline must close gracefully without errors |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M121
