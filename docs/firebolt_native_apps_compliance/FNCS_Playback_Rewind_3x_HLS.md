# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_100**

## TestCase Name
**FNCS_Playback_Rewind_3x_HLS**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that HLS adaptive streaming content supports rewind playback at 3x speed (negative playback rate), ensuring proper backward playback at accelerated speed with correct adaptive bitrate handling during rewind operations.

**VIDEO CODEC:** H264

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | HLS stream (TDK_Asset_HLS_Stream.m3u8) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for rewind playback operation. Default value is 10 seconds |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Rewind 3x Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve HLS stream URL from MediaValidationVariables library. Construct mediapipelinetests command with trickplay operation specifying negative playback rate of -3.0. Execute command: `tdk_mediapipelinetests_trickplay https://<server_hosting_stream>:<port_number>/TDK_Asset_HLS_Stream.m3u8 checkavstatus=<yes/no> playbackRate=-3.0` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with negative playback rate. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins HLS adaptive stream playback using GStreamer playbin element with westeros-sink for rendering at normal playback speed | HLS adaptive stream playback must begin successfully without pipeline errors |
| 4 | Set Playback Rate to Rewind 3x | Configure the playbin element to transition to negative playback rate of -3.0x. Verify that playback direction changes to backward and speed increases to 3x | Playback rate must change to -3.0x successfully. Playback must transition to backward direction smoothly |
| 5 | Monitor Backward Playback at 3x Speed | Monitor video rendering during rewind playback at 3x speed. Verify that video frames render in reverse direction at accelerated pace. Verify playback position decreases over time at approximately 3x the normal rate | Video must render in backward direction. Position must decrease smoothly at 3x speed. No pipeline errors should occur during rewind playback |
| 6 | Verify Video Frame Rendering Quality | Monitor video rendering using westerossink "stats" property. Verify video frames are rendered with acceptable drop rate. Monitor that video frame drop rate does not exceed 1% during rewind operation | Video frames must render continuously. Frame drop rate must remain below 1% throughout rewind playback |
| 7 | Verify Smooth Playback Transition | Confirm that rewind playback at 3x speed continues smoothly without interruptions or video glitches until reaching the beginning of stream or timeout | Video playback must continue seamlessly throughout rewind operation without interruption |
| 8 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify that rewind operation completed successfully | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Rewind operation must be confirmed as successful |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M121
