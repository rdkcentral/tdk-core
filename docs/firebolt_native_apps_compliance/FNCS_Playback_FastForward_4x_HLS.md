# FNCS_Playback_FastForward_4x_HLS Test Documentation

## TestCase ID
FNCS_PLAYBACK_49

## TestCase Name
FNCS_Playback_FastForward_4x_HLS

## Table Of Contents
1. [TestCase ID](#testcase-id)
2. [TestCase Name](#testcase-name)
3. [Objective](#objective)
4. [Preconditions](#preconditions)
5. [Test Steps](#test-steps)
6. [Test Attributes](#test-attributes)

## Objective
This test validates the fast forward playback functionality at 4x rate for HLS (HTTP Live Streaming) content to ensure proper trick-play operations and adaptive streaming pipeline handling during accelerated playback scenarios.

**VIDEO CODEC:** HLS Adaptive Streaming

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | TDK_FNCS_Package must be installed in DUT |
| 2 | video_src_url_hls stream must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://&lt;server_hosting_stream&gt;:&lt;port_number&gt;/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration must be set (yes/no) in device config file to enable or disable SOC level AV playback verification |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration must be set to specify timeout duration for media playback validation |
| 5 | FIREBOLT_COMPLIANCE_FASTFORWARD_3x_4x_ENABLED configuration must be set to "yes" to enable 4x fast forward support |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Validate 4x Support Configuration | Retrieve FIREBOLT_COMPLIANCE_FASTFORWARD_3x_4x_ENABLED configuration value to verify device supports 4x fast forward operations | Configuration value must be retrieved successfully and should be "yes" for test to proceed |
| 3 | Execute Fast Forward 4x Test | Retrieve configuration values for AV status check and playback timeout, obtain HLS stream URL from MediaValidationVariables, construct trickplay test command with fastforward4x operations, and execute the command `tdk_mediapipelinetests_trickplay https://&lt;server_hosting_stream&gt;:&lt;port_number&gt;/[STREAM_NAME] checkavstatus=no operations=fastforward4x:10` | Configuration values must be retrieved successfully, stream URL must be obtained correctly, command must be constructed properly, test command execution must start successfully and test application starts execution without errors |
| 4 | Monitor Fast Forward HLS Playback | Monitor HLS adaptive streaming playback during 4x fast forward operation to verify proper segment fetching, frame rendering, timeline progression, and playback rate acceleration | HLS content must render properly at 4x fast forward rate with smooth adaptive streaming, timeline progression and accelerated playback without errors |
| 5 | Validate Test Completion | Verify test execution completes successfully by checking output for success indicators "Failures: 0" and "Errors: 0" or "failed: 0" | Test output must contain success indicators confirming fast forward 4x operation completed successfully without failures or errors |

## Test Attributes
**Supported Models:** Video_Accelerator  
**Estimated Duration:** 3 minutes  
**Priority:** High  
**Release Version:** M136