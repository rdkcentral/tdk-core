# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_252**

## TestCase Name
**FNCS_Playback_SeekForward_FF2x_H264_24Fps**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that a 24 Fps H264 stream supports forward seek operation followed by fast-forward playback at 2x speed, ensuring proper seeking accuracy and fast playback with correct frame rate management.

**VIDEO CODEC:** H264 (24 Fps)

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | H264 24Fps DASH stream (TDK_Asset_H264_24Fps_DASH_Stream.mpd) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for which the fast forward operation should be carried out. Default value is 10 seconds |
| 5 | FIREBOLT_COMPLIANCE_SEEK_POSITION configuration variable specifies the target position in seconds where the seek operation should be performed. Default value is 30 seconds |
| 6 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration variable enables full playback validation including position, frame rendering, and PTS synchronization. Default value is "no" |
| 7 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration variable enables video presentation timestamp (PTS) validation to verify smooth playback timing. Default value is "no" |
| 8 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration variable enables frame rate verification to ensure the stream maintains 24 Fps during playback. Default value is "no" |
| 9 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration variable enables audio frame monitoring for audio-video synchronization verification. Default value is "no" |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Seek Forward FF2x Test | Retrieve all configuration values (FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, FIREBOLT_COMPLIANCE_SEEK_POSITION, FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK, FIREBOLT_COMPLIANCE_CHECK_PTS, FIREBOLT_COMPLIANCE_CHECK_FPS, FIREBOLT_COMPLIANCE_CHECK_AUDIO) from Device config file. Retrieve H264 24Fps DASH stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_trickplay operation specifying seek and fastForward2x operations. Execute command: `tdk_mediapipelinetests_trickplay https://<server_hosting_stream>:<port_number>/TDK_Asset_H264_24Fps_DASH_Stream.mpd checkavstatus=<yes/no> operations=seek:<seek_position> fastForward2x:<timeout>` | All configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly. Test application must start execution without errors |
| 3 | Verify Playback Starts | Validate that the mediapipeline initializes and begins H264 24Fps stream playback using GStreamer playbin element with westeros-sink for rendering | H264 24Fps stream playback must begin successfully without pipeline errors |
| 4 | Execute Forward Seek Operation | Perform a forward seek operation to the position specified by FIREBOLT_COMPLIANCE_SEEK_POSITION (default 30 seconds). Verify seek completion and confirm playback position is at the target seek location | Seek operation must complete successfully. Playback position must be at or near the specified seek position. No pipeline errors should occur |
| 5 | Apply Fast Forward 2x Rate | Execute the fastForward2x operation which increases the playback rate to 200% of normal speed (2x rate), adjusting frame delivery to approximately 48 Fps (24 Fps × 2) after the seek operation completes | Playback rate must transition to 2x successfully following the seek. Media continues playing at doubled speed with adjusted frame rate |
| 6 | Monitor Fast Forward Playback Position | Monitor playback position progression during fast-forward operation for the configured timeout duration (default 10 seconds). Verify playback position increments occur at 2x rate. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder status | Playback position must progress at 2x rate smoothly. If AV status check is enabled, video decoder must show active decoding without interruptions |
| 7 | Verify Frame Rate During Fast Forward | If FIREBOLT_COMPLIANCE_CHECK_FPS is enabled, monitor the delivered frame rate during fast-forward playback. Verify the stream maintains approximately 48 Fps (24 Fps × 2x rate) during the fast-forward operation | Frame rate during fast-forward must be approximately 48 Fps with acceptable variance. Frame rate validation must complete without errors |
| 8 | Verify Video PTS Synchronization | If FIREBOLT_COMPLIANCE_CHECK_PTS is enabled, use westerossink "video-pts" property to obtain presentation timestamps each millisecond. Monitor for smooth playback timing and verify PTS progression matches the 2x playback rate | Video PTS values must progress smoothly at 2x rate intervals. PTS synchronization must show no gaps or jumps |
| 9 | Verify Playback Quality During Fast Forward | Verify that video frames are rendered correctly during fast-forward using westerossink "stats" property to monitor frames rendered and dropped. Monitor that frame drop rate does not exceed 1% during the fast-forward operation | Video frames must render continuously with frame drop rate less than 1% |
| 10 | Validate Audio Synchronization | If FIREBOLT_COMPLIANCE_CHECK_AUDIO is enabled, use native audio-sink "stats" property to obtain audio frames rendered and dropped. Verify audio synchronization with video during fast-forward playback and ensure audio drop rate does not exceed 1% | Audio frames must render synchronously with video. Audio drop rate must not exceed 1% |
| 11 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify pipeline closes cleanly after fast-forward timeout expires | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Pipeline must close gracefully without errors |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M123
