# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_67**

## TestCase Name
**FNCS_Playback_PlaySeek_Forward_Stress_H264**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that an H264 stream supports multiple forward seek operations during playback with incremental seek positions, ensuring proper seeking accuracy under stress conditions and consistent smooth playback resumption across repeated seek operations.

**VIDEO CODEC:** H264

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | H264 DASH stream (TDK_Asset_H264_DASH_Stream.mpd) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for playback between seek operations. Default value is 10 seconds |
| 5 | FIREBOLT_COMPLIANCE_SEEK_STEP configuration variable specifies the incremental position in seconds to advance for each seek operation iteration. Default value is 30 seconds |
| 6 | FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT configuration variable specifies the number of forward seek iterations to perform. Default value is 3 |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Stress Forward Seek Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, FIREBOLT_COMPLIANCE_SEEK_STEP, and FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT configuration values from Device config file. Retrieve H264 DASH stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_playseek operation specifying multiple forward seek operations with incremental seek positions. Execute command: `tdk_mediapipelinetests_playseek https://<server_hosting_stream>:<port_number>/TDK_Asset_H264_DASH_Stream.mpd checkavstatus=<yes/no> operations=seek:<seek_step>,seek:<seek_step*2>,seek:<seek_step*3>` (repeat count iterations) | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with all seek iterations. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins H264 stream playback using GStreamer playbin element with westeros-sink for rendering | H264 stream playback must begin successfully without pipeline errors |
| 4 | Execute First Forward Seek Operation | Perform the first forward seek operation to the position specified by FIREBOLT_COMPLIANCE_SEEK_STEP (default 30 seconds). Verify seek completion and confirm playback position is at the target seek location | First forward seek operation must complete successfully. Playback position must be at or near the specified seek position. No pipeline errors should occur |
| 5 | Verify Playback Resumes After First Seek | Confirm that playback resumes smoothly at the new position after the first seek operation completes | Media playback must continue seamlessly from the seek position without interruption |
| 6 | Execute Second Forward Seek Operation | Perform the second forward seek operation to the position specified by FIREBOLT_COMPLIANCE_SEEK_STEP × 2. Verify seek completion and confirm playback position is at the new target seek location | Second forward seek operation must complete successfully. Playback position must be at or near the specified seek position. No pipeline errors should occur |
| 7 | Verify Playback Resumes After Second Seek | Confirm that playback resumes smoothly at the new position after the second seek operation completes | Media playback must continue seamlessly from the new seek position without interruption |
| 8 | Execute Third Forward Seek Operation | Perform the third forward seek operation to the position specified by FIREBOLT_COMPLIANCE_SEEK_STEP × 3. Verify seek completion and confirm playback position is at the new target seek location | Third forward seek operation must complete successfully. Playback position must be at or near the specified seek position. No pipeline errors should occur |
| 9 | Verify Playback Resumes After Third Seek | Confirm that playback resumes smoothly at the new position after the third seek operation completes | Media playback must continue seamlessly from the seek position without interruption |
| 10 | Monitor Overall Playback Quality | Monitor playback quality throughout all seek iterations. Verify video frame rendering using westerossink "stats" property. Monitor that frame drop rate does not exceed 1% across all iterations. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder status remains active throughout stress test | Video frames must render continuously with frame drop rate less than 1% throughout all seek iterations. If AV status check is enabled, video decoder must show active decoding without interruptions |
| 11 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify pipeline closes cleanly after all stress iterations complete | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Pipeline must close gracefully without errors |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 5 minutes

**Priority:** High

**Release Version:** M121
