# Test Case Documentation

## TestCase ID
**FNCS_PLAYBACK_209**

## TestCase Name
**FNCS_Playback_SeekForward_FF2x_AAC**

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name)
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
To validate that an audio-only AAC stream supports forward seek operation followed by fast-forward playback at 2x speed, ensuring proper seeking accuracy and fast audio playback rate transitions.

**AUDIO CODEC:** AAC

## Preconditions

| ID | Conditions |
|----|-----------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | AAC audio stream (TDK_Asset_AAC_Audio_Stream.m4a) must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration variable specifies whether SOC level playback verification check should be done or not. Default value is "no" |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration variable specifies the duration in seconds for which the fast forward operation should be carried out. Default value is 10 seconds |
| 5 | FIREBOLT_COMPLIANCE_SEEK_POSITION configuration variable specifies the target position in seconds where the seek operation should be performed. Default value is 30 seconds |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|---|---|---|---|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Configure and Execute Seek Forward FF2x Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_SEEK_POSITION configuration values from Device config file. Retrieve AAC stream URL from MediaValidationVariables library. Construct mediapipelinetests command with test_trickplay operation specifying seek and fastForward2x operations. Execute command: `tdk_mediapipelinetests_trickplay https://<server_hosting_stream>:<port_number>/TDK_Asset_AAC_Audio_Stream.m4a checkavstatus=<yes/no> operations=seek:<seek_position> fastForward2x:<timeout>` | Configuration values must be retrieved successfully. Stream URL must be obtained correctly. Command must be constructed properly. Test application must start execution without errors |
| 3 | Verify Playback Starts | Validate that the mediapipeline initializes and begins AAC audio stream playback using GStreamer playbin element with native audio sink for rendering | AAC audio playback must begin successfully without pipeline errors. Audio sink must be properly initialized |
| 4 | Execute Forward Seek Operation | Perform a forward seek operation to the position specified by FIREBOLT_COMPLIANCE_SEEK_POSITION (default 30 seconds). Verify seek completion and confirm playback position is at the target seek location | Seek operation must complete successfully. Playback position must be at or near the specified seek position. No pipeline errors should occur |
| 5 | Apply Fast Forward 2x Rate | Execute the fastForward2x operation which increases the playback rate to 200% of normal speed (2x rate) after the seek operation completes | Playback rate must transition to 2x successfully following the seek. Audio continues playing at doubled speed (pitch-shifted) without stuttering |
| 6 | Monitor Fast Forward Audio Playback | Monitor playback position progression during fast-forward operation for the configured timeout duration (default 10 seconds). Verify playback position increments occur at 2x rate. If FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is enabled, verify SOC level audio decoder status | Playback position must progress at 2x rate smoothly. If AV status check is enabled, audio decoder must show active decoding without interruptions |
| 7 | Verify Audio Quality During Fast Forward | Monitor native audio-sink "stats" property to obtain audio frames rendered and dropped. Verify audio rendering continues smoothly during fast-forward playback and ensure audio drop rate does not exceed 1% | Audio frames must render continuously with audio drop rate less than 1% |
| 8 | Validate Test Completion | Check output from mediapipelinetests application for success indicators containing "Failures: 0" and "Errors: 0" or "failed: 0" string. Verify pipeline closes cleanly after fast-forward timeout expires | Test application output must contain "Failures: 0" and "Errors: 0" or "failed: 0". Pipeline must close gracefully without errors |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M121
