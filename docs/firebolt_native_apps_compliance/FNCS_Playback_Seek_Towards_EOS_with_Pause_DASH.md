# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_265**

## TestCase Name
**FNCS_Playback_Seek_Towards_EOS_with_Pause_DASH**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that DASH adaptive streaming content supports pause and resume operations on streams that have been seeked towards the end, and properly detects the End Of Stream (EOS) signal after resuming from pause near stream end, ensuring correct playback state transitions and stream termination handling.

**VIDEO CODEC:** H.264

**AUDIO CODEC:** AAC

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | DASH stream (TDK_Asset_H264_Bitrate_DASH_Stream.mpd) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for playback after seek and pause operations. Default value is 10 seconds |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Seek Towards EOS with Pause Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve DASH stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_seek_EOS_with_pause operation specifying seek position near end of stream. Execute command: `tdk_mediapipelinetests_seek https://<server_hosting_stream>:<port_number>/TDK_Asset_H264_Bitrate_DASH_Stream.mpd checkavstatus=<yes/no> operations=seek:eos,pause:5,resume` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with EOS seek, pause, and resume operations. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins DASH adaptive stream playback using GStreamer playbin element with westeros-sink for rendering and native audio-sink for audio | DASH adaptive stream playback must begin successfully without pipeline errors |
| 4 | Execute Seek Towards End Of Stream | Perform seek operation targeting the end of stream (position near EOS). Verify seek operation completes and playback position advances to near stream end | Seek towards EOS must complete successfully. Playback position must be at or near the end of the stream |
| 5 | Execute Pause Operation | Pause playback at the current position near stream end. Verify that playback stops and pipeline transitions to PAUSED state without errors | Playback must pause successfully. Pipeline state must transition to PAUSED state |
| 6 | Verify Pause State | Confirm that the pipeline remains in PAUSED state while paused. Verify playback position does not advance while paused | Pipeline must remain in PAUSED state. Playback position must remain constant during pause |
| 7 | Execute Resume Operation | Resume playback from the paused position. Verify that playback restarts smoothly from the paused position towards the stream end | Playback must resume successfully from the paused position. Media must continue towards stream termination |
| 8 | Monitor Playback Until EOS | Continue monitoring playback after resume operation until stream reaches end. Verify smooth playback without interruption or frame drops during resume-to-EOS playback | Playback must continue smoothly. No interruptions or pipeline errors should occur |
| 9 | Verify End Of Stream Detection | Monitor GStreamer pipeline for EOS (End Of Stream) message signal. Verify that EOS message is detected after resuming playback and stream reaches end. Confirm pipeline state transitions to READY or NULL after EOS | EOS message must be detected by the mediapipelinetests application. Pipeline must handle EOS gracefully after pause/resume cycle |
| 10 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify pause/resume and EOS operations were completed successfully | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". All pause, resume, and EOS operations must be confirmed in output logs |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M124
