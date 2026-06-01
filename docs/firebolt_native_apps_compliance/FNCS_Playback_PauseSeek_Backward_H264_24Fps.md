# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_241**

## TestCase Name
**FNCS_Playback_PauseSeek_Backward_H264_24Fps**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that DASH stream playback with H264 video codec at 24 frames per second supports backward seek operations after pause with full playback validation, PTS monitoring, and frame rate verification, ensuring proper playback state transitions from paused state to the beginning position and resumption of playback at the specified frame rate.

**VIDEO CODEC:** H264 (24 Fps)

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | H264 24Fps DASH stream (TDK_Asset_H264_DASH_24Fps_Stream.mpd) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for playback operations. Default value is 10 seconds |
| 5 | FIREBOLT_COMPLIANCE_SEEK_POSITION configuration variable specifies the target position in seconds for backward seek operation. Default value is 0 seconds (beginning of stream) |
| 6 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration variable enables extended full playback validation. Default value is "no" |
| 7 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration variable enables PTS (Presentation Time Stamp) validation for timing accuracy. Default value is "no" |
| 8 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration variable enables frame rate verification and monitoring. Default value is "no" |
| 9 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration variable enables audio frame rendering and drop rate validation. Default value is "no" |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Pause-Seek-Play Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, FIREBOLT_COMPLIANCE_SEEK_POSITION, FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK, FIREBOLT_COMPLIANCE_CHECK_PTS, FIREBOLT_COMPLIANCE_CHECK_FPS, and FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration values from Device config file. Retrieve H264 24Fps DASH stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_trickplay operation specifying pause, backward seek, and play operations with extended validation flags. Execute command: `tdk_mediapipelinetests_trickplay https://<server_hosting_stream>:<port_number>/TDK_Asset_H264_DASH_24Fps_Stream.mpd checkavstatus=<yes/no> operations=pause:5,seek:0,play:10 validate_full_playback=<yes/no> check_pts=<yes/no> check_fps=<yes/no> check_audio=<yes/no>` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly with pause, seek, play, and extended validation operations. Test application must start execution without errors |
| 3 | Verify Initial Playback Starts | Validate that the mediapipeline initializes and begins H264 24Fps DASH stream playback using GStreamer playbin element with westeros-sink for rendering | H264 24Fps DASH stream playback must begin successfully without pipeline errors |
| 4 | Execute Pause Operation | Transition playbin to PAUSED state. Verify that playback stops and pipeline transitions to PAUSED state. Monitor pause duration (5 seconds) | Pipeline must transition to PAUSED state successfully. Playback must stop smoothly |
| 5 | Execute Backward Seek Operation | From the paused state, execute backward seek to position 0 (beginning of stream). Verify that seek operation completes and pipeline remains in valid state without errors | Seek operation must complete successfully. Pipeline must transition to seek target position. Playback position must update to approximately 0 seconds |
| 6 | Resume Playback After Seek | Transition playbin from paused state to PLAYING state after seek completion. Monitor playback for the configured timeout duration (default 10 seconds). Verify video frames render smoothly from the beginning at 24 Fps | Playback must resume successfully from the beginning. Video frames must render continuously at 24 Fps without interruption |
| 7 | Validate Presentation Time Stamps | If FIREBOLT_COMPLIANCE_CHECK_PTS is enabled, monitor video-pts property from westerossink each millisecond to validate smooth timing progression and absence of timing gaps or discontinuities | PTS values must progress smoothly without timing gaps. All presentation timestamps must be within expected range for 24 Fps content |
| 8 | Validate Frame Rate Accuracy | If FIREBOLT_COMPLIANCE_CHECK_FPS is enabled, verify that video frame rendering maintains 24 Fps rate throughout playback without deviations. Monitor frame delivery rate each second | Frame rate must remain at 24 Fps throughout test. Deviation from target frame rate must not exceed acceptable tolerance |
| 9 | Monitor Audio Frame Rendering | If FIREBOLT_COMPLIANCE_CHECK_AUDIO is enabled, monitor native audio-sink "stats" property to obtain audio frames rendered and dropped throughout pause, seek, and play operations | Audio frames must render with drop rate below 1%. Audio output must synchronize with video playback |
| 10 | Monitor Overall Playback Quality | Monitor video frame rendering using westerossink "stats" property throughout all operations. Verify that video frame drop rate does not exceed 1% across all state transitions. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder remains active | Video frames must render with drop rate below 1%. All state transitions must occur without pipeline errors. If AV status check is enabled, video decoder must show continuous activity |
| 11 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify pause, seek, play, and all extended validation operations completed successfully | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". All trickplay and validation operations must be confirmed as successful |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M122
