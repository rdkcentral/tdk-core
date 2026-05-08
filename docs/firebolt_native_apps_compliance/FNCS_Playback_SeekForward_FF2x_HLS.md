# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_210**

## TestCase Name
**FNCS_Playback_SeekForward_FF2x_HLS**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that an HLS streaming stream supports forward seek operation followed by fast-forward playback at 2x speed, ensuring proper seeking accuracy in adaptive streaming and fast playback rate transitions.

**VIDEO CODEC:** HLS (Adaptive Streaming)

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | HLS stream (TDK_Asset_HLS_Stream.m3u8) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for which the fast forward operation should be carried out. Default value is 10 seconds |
| 5 | FIREBOLT_COMPLIANCE_SEEK_POSITION configuration variable specifies the target position in seconds where the seek operation should be performed. Default value is 30 seconds |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Seek Forward FF2x Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_SEEK_POSITION configuration values from Device config file. Retrieve HLS stream URL (TDK_Asset_HLS_Stream.m3u8) from MediaValidationVariables library. Construct mediapipelinetests command with test_trickplay operation specifying seek and fastForward2x operations. Execute command: `tdk_mediapipelinetests_trickplay https://<server_hosting_stream>:<port_number>/TDK_Asset_HLS_Stream.m3u8 checkavstatus=<yes/no> operations=seek:<seek_position> fastForward2x:<timeout>` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly. Test application must start execution without errors |
| 3 | Verify Playback Starts | Validate that the mediapipeline initializes and begins HLS stream playback using GStreamer playbin element with westeros-sink for rendering. Verify HLS stream parsing and adaptive bitrate management | HLS stream playback must begin successfully without pipeline errors. Adaptive streaming initialization must complete |
| 4 | Execute Forward Seek Operation | Perform a forward seek operation to the position specified by FIREBOLT_COMPLIANCE_SEEK_POSITION (default 30 seconds) in the HLS stream. Verify seek completion by updating playlist position and confirm playback position is at the target seek location | Seek operation must complete successfully. HLS playlist must be updated correctly. Playback position must be at or near the specified seek position. No pipeline errors should occur |
| 5 | Apply Fast Forward 2x Rate | Execute the fastForward2x operation which increases the playback rate to 200% of normal speed (2x rate) after the seek operation completes | Playback rate must transition to 2x successfully following the seek. Media continues playing at doubled speed without stuttering or buffering interruptions |
| 6 | Monitor Fast Forward Playback | Monitor playback position progression during fast-forward operation for the configured timeout duration (default 10 seconds). Verify playback position increments occur at 2x rate. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level video decoder status | Playback position must progress at 2x rate smoothly. If AV status check is enabled, video decoder must show active decoding without interruptions |
| 7 | Verify Playback Quality During Fast Forward | Verify that video frames are rendered correctly during fast-forward using westerossink "stats" property to monitor frames rendered and dropped. Monitor that frame drop rate does not exceed 1% during the fast-forward operation. Verify adaptive bitrate stream selection during fast playback | Video frames must render continuously with frame drop rate less than 1%. Bitrate switching should be seamless |
| 8 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify pipeline closes cleanly after fast-forward timeout expires | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Pipeline must close gracefully without errors |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M121
