# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_70**

## TestCase Name
**FNCS_Playback_PlaySeek_Backward_Stress_DASH**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that DASH adaptive streaming content supports multiple backward seek operations during playback, ensuring proper seeking accuracy under stress conditions with correct media delivery over adaptive streaming protocol.

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | DASH stream (TDK_Asset_DASH_Stream.mpd) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for playback between seek operations. Default value is 10 seconds |
| 5 | FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT configuration variable specifies the number of backward seek iterations to perform. Default value is 3 |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Stress Backward Seek Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_STRESS_REPEAT_COUNT configuration values from Device config file. Retrieve DASH stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_playseek operation specifying multiple backward seek operations. Execute command: `tdk_mediapipelinetests_playseek https://<server_hosting_stream>:<port_number>/TDK_Asset_DASH_Stream.mpd checkavstatus=<yes/no> operations=seek:0,seek:0,seek:0` (repeat count iterations) | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with all seek iterations. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins DASH adaptive stream playback using GStreamer playbin element with westeros-sink for rendering and native audio-sink for audio | DASH adaptive stream playback must begin successfully without pipeline errors |
| 4 | Execute First Backward Seek Operation | Perform the first backward seek operation to the beginning of the stream (position 0). Verify seek completion and confirm playback position is at the start of the stream | First backward seek operation must complete successfully. Playback position must be at or near the beginning of the stream. No pipeline errors should occur |
| 5 | Verify Playback Resumes After First Seek | Confirm that playback resumes smoothly at the beginning position after the first seek operation completes | Media playback must continue seamlessly from the beginning position without interruption |
| 6 | Execute Second Backward Seek Operation | Perform the second backward seek operation to the beginning of the stream (position 0). Verify seek completion and confirm playback position is at the start of the stream | Second backward seek operation must complete successfully. Playback position must be at or near the beginning of the stream. No pipeline errors should occur |
| 7 | Verify Playback Resumes After Second Seek | Confirm that playback resumes smoothly at the beginning position after the second seek operation completes | Media playback must continue seamlessly from the beginning position without interruption |
| 8 | Execute Third Backward Seek Operation | Perform the third backward seek operation to the beginning of the stream (position 0). Verify seek completion and confirm playback position is at the start of the stream | Third backward seek operation must complete successfully. Playback position must be at or near the beginning of the stream. No pipeline errors should occur |
| 9 | Verify Playback Resumes After Third Seek | Confirm that playback resumes smoothly at the beginning position after the third seek operation completes | Media playback must continue seamlessly from the beginning position without interruption |
| 10 | Monitor Overall Playback Quality | Monitor playback quality throughout all seek iterations. Verify video frame rendering using westerossink "stats" property and audio rendering using native audio-sink "stats" property. Monitor that frame and audio drop rates do not exceed 1% across all iterations. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level decoders remain active throughout stress test | Video and audio frames must render continuously with drop rates less than 1% throughout all seek iterations. If AV status check is enabled, decoders must show active decoding without interruptions |
| 11 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify pipeline closes cleanly after all stress iterations complete | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Pipeline must close gracefully without errors |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 5 minutes

**Priority:** High

**Release Version:** M121
