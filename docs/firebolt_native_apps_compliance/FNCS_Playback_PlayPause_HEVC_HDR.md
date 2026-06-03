# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_88**

## TestCase Name
**FNCS_Playback_PlayPause_HEVC_HDR**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that HEVC video codec in HDR format supports stable play and pause operations through the GStreamer media pipeline, ensuring correct state transitions and robust pipeline management with HDR content rendering.

**VIDEO CODEC:** HEVC

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | HEVC HDR stream (TDK_Asset_HEVC_HDR_Stream.mp4) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the timeout in seconds for video playback verification. Default value is "10" |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Play-Pause Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration values from Device config file. Retrieve HEVC HDR stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_play_pause_pipeline operation. Execute command: `tdk_mediapipelinetests_pipeline https://<server_hosting_stream>:<port_number>/TDK_Asset_HEVC_HDR_Stream.mp4 checkavstatus=<yes/no> timeout=<seconds>` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly. Test application must start execution without errors |
| 3 | Create GStreamer Pipeline with Playbin | Initialize GStreamer pipeline infrastructure and create playbin element for unified media handling. Configure playbin to auto-detect and initialize HEVC video decoder and set westerossink as video rendering sink for HDR content | GStreamer pipeline must be created successfully. Playbin element must initialize with proper HEVC decoder plugin. Video sink element must be configured for HDR rendering without errors |
| 4 | Set Pipeline to PLAYING State | Transition the GStreamer pipeline from NULL state to READY state, then to PAUSED state, and finally to PLAYING state. During transitions, establish connection to stream and begin decoder initialization. Verify that HEVC video decoder initializes and begins rendering HDR video frames | Pipeline state transitions must succeed at each stage. Stream connection must establish successfully. HEVC decoder must initialize and render HDR frames |
| 5 | Monitor Playback in PLAYING State | Verify that HDR video frames render continuously using westerossink "stats" property to monitor frame rendering rate. Verify that HDR metadata is properly processed for correct color mapping and rendering. Maintain PLAYING state for configured timeout duration | HDR video frames must render continuously and smoothly. HDR color information must be correctly applied to rendered frames. Frame drop rate must remain below 1% during playback |
| 6 | Transition Pipeline to PAUSED State | Issue explicit command to transition playbin from PLAYING to PAUSED state. Verify that video frame rendering stops cleanly while maintaining decoder state and current playback position | Pipeline must transition to PAUSED state successfully. HDR video rendering must stop immediately. Current playback position must be maintained |
| 7 | Resume Playback from Paused State | Transition playbin from PAUSED state back to PLAYING state. Verify that HDR video rendering resumes from the paused position with correct HDR frame rendering | Pipeline must transition from PAUSED to PLAYING state successfully. HDR video frames must resume rendering from paused position without interruption |
| 8 | Transition Pipeline to PAUSED State Again | Perform second pause operation to ensure consistent pause behavior under HDR playback conditions | Second pause operation must succeed cleanly. Pipeline must remain stable |
| 9 | Monitor Overall Pipeline Quality | Throughout all state transitions, monitor westerossink "stats" property for video frame drop rates. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder activity during all state transitions. Verify that HDR processing remains consistent throughout pipeline operations | Video frame drop rate must remain below 1% across all states. All state transitions must complete without errors. If AV status is enabled, video decoder must show continuous activity |
| 10 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0" |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
