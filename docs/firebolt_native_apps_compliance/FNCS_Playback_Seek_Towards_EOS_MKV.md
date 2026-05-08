# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_318**

## TestCase Name
**FNCS_Playback_Seek_Towards_EOS_MKV**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that MKV container format content with AV1 video codec supports seek operations towards the end of stream and properly detects the End Of Stream (EOS) signal after seeking near the stream end, ensuring correct stream termination handling for MKV media files.

**VIDEO CODEC:** AV1

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | MKV stream (TDK_Asset_4K_AV1_Stream.mkv) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for playback after seek operation. Default value is 10 seconds |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Seek Towards EOS Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve MKV stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_seek_EOS operation specifying seek position near end of stream. Execute command: `tdk_mediapipelinetests_seek https://<server_hosting_stream>:<port_number>/TDK_Asset_4K_AV1_Stream.mkv checkavstatus=<yes/no> operations=seek:eos` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with EOS seek operation. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins MKV stream playback using GStreamer playbin element with westeros-sink for rendering | MKV stream playback must begin successfully without pipeline errors |
| 4 | Execute Seek Towards End Of Stream | Perform seek operation targeting the end of stream (position near EOS). Verify seek operation completes and playback position advances to near stream end | Seek towards EOS must complete successfully. Playback position must be at or near the end of the stream |
| 5 | Verify Playback Resumes After Seek | Confirm that playback continues smoothly from the seek position towards the stream end without interruption | Media playback must continue seamlessly from the seek position towards stream termination |
| 6 | Verify End Of Stream Detection | Monitor GStreamer pipeline for EOS (End Of Stream) message signal. Verify that EOS message is detected when stream reaches the end after seek operation. Confirm pipeline state transitions to READY or NULL after EOS | EOS message must be detected by the mediapipelinetests application. Pipeline must handle EOS gracefully and transition states appropriately |
| 7 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify EOS was detected in test log output | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". EOS detection must be confirmed in output logs |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 2 minutes

**Priority:** High

**Release Version:** M132
