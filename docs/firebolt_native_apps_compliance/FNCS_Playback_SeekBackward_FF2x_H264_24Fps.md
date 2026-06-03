# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_251**

## TestCase Name
**FNCS_Playback_SeekBackward_FF2x_H264_24Fps**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that a 24 Fps H264 stream supports backward seek operation followed by fast-forward playback at 2x speed, with extended validation of video presentation timestamps, frame rates, and audio synchronization to ensure proper seeking accuracy and fast playback with correct media delivery.

**VIDEO CODEC:** H264 (24 Fps)

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | H264 24Fps DASH stream (TDK_Asset_H264_24Fps_DASH_Stream.mpd) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for which the fast forward operation should be carried out. Default value is 10 seconds |
| 5 | FIREBOLT_COMPLIANCE_SEEK_POSITION configuration variable specifies the target position in seconds where the seek operation should be performed. Default value is 30 seconds |
| 6 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration variable specifies whether extended playback validation should be performed. Default value is "yes" |
| 7 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration variable specifies whether presentation timestamp validation should be performed. Default value is "yes" |
| 8 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration variable specifies whether frame rate validation should be performed. Default value is "yes" |
| 9 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration variable specifies whether audio frame validation should be performed. Default value is "yes" |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Seek Backward FF2x Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, FIREBOLT_COMPLIANCE_SEEK_POSITION, FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK, FIREBOLT_COMPLIANCE_CHECK_PTS, FIREBOLT_COMPLIANCE_CHECK_FPS, and FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration values from Device config file. Retrieve H264 24Fps DASH stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_trickplay operation specifying seek and fastForward2x operations. Execute command: `tdk_mediapipelinetests_trickplay https://<server_hosting_stream>:<port_number>/TDK_Asset_H264_24Fps_DASH_Stream.mpd checkavstatus=<yes/no> operations=seek:<seek_position> fastForward2x:<timeout>` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly. Test application must start execution without errors |
| 3 | Verify Playback Starts | Validate that the mediapipeline initializes and begins H264 24Fps stream playback using GStreamer playbin element with westeros-sink for rendering | H264 24Fps stream playback must begin successfully without pipeline errors |
| 4 | Execute Backward Seek Operation | Perform a backward seek operation from the current playback position to a position specified by FIREBOLT_COMPLIANCE_SEEK_POSITION (default 30 seconds earlier). Verify seek completion and confirm playback position is at the target seek location | Backward seek operation must complete successfully. Playback position must be at or near the specified seek position. No pipeline errors should occur |
| 5 | Apply Fast Forward 2x Rate | Execute the fastForward2x operation which increases the playback rate to 200% of normal speed (2x rate), adjusting frame delivery to 48 Fps (24 Fps × 2) after the backward seek operation completes | Playback rate must transition to 2x successfully following the seek. Media continues playing at doubled speed with adjusted frame rate |
| 6 | Monitor Fast Forward Playback | Monitor playback position progression during fast-forward operation for the configured timeout duration (default 10 seconds). Verify playback position increments occur at 2x rate. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder status | Playback position must progress at 2x rate smoothly. If AV status check is enabled, video decoder must show active decoding without interruptions |
| 7 | Verify Video Frame Rendering During Fast Forward | Verify that video frames are rendered correctly during fast-forward using westerossink "stats" property to monitor frames rendered and dropped. Monitor that frame drop rate does not exceed 1% during the fast-forward operation | Video frames must render continuously with frame drop rate less than 1% |
| 8 | Validate Video Presentation Timestamps | If FIREBOLT_COMPLIANCE_CHECK_PTS is enabled, monitor video presentation timestamps using westerossink "video-pts" property each millisecond. Verify that PTS values progress smoothly during fast-forward playback at 2x speed, indicating proper timing synchronization | Video PTS must progress smoothly without gaps or jumps, confirming proper video timing during fast-forward |
| 9 | Validate Frame Rate During Fast Forward | If FIREBOLT_COMPLIANCE_CHECK_FPS is enabled, verify that the frame rate during fast-forward matches the expected 48 Fps (24 Fps × 2). Monitor frame delivery rate to confirm it maintains fast-forward speed requirements | Frame rate must be maintained at 48 Fps throughout the fast-forward operation |
| 10 | Validate Audio Synchronization | If FIREBOLT_COMPLIANCE_CHECK_AUDIO is enabled, verify audio frame rendering using native audio-sink "stats" property. Monitor audio frames rendered and dropped during fast-forward. Verify audio drop rate does not exceed 1% and audio synchronization with video is maintained | Audio frames must render continuously with drop rate less than 1%, maintaining synchronization with video fast-forward |
| 11 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify pipeline closes cleanly after fast-forward timeout expires | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Pipeline must close gracefully without errors |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M123
