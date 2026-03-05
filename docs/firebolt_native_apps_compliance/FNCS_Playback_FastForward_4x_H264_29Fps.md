# FNCS_Playback_FastForward_4x_H264_29Fps

## TestCase ID
FNCS_PLAYBACK_231

## TestCase Name
FNCS_Playback_FastForward_4x_H264_29Fps

## Table Of Contents
- [TestCase ID](#testcase-id)
- [TestCase Name](#testcase-name) 
- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to validate fast forward operation at 4x playback rate for H264 29fps video content to ensure smooth trick play functionality without playback issues at standard frame rate.

**VIDEO CODEC:** H264

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | TDK_FNCS_Package should be installed in DUT |
| 2 | tdk_mediapipelinetests application must be installed in DUT |
| 3 | video_src_url_dash_h264_29fps must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc. Users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://&lt;server_hosting_stream&gt;:&lt;port_number&gt;/) based on their setup preference |
| 4 | FIREBOLT_COMPLIANCE_FASTFORWARD_3x_4x_ENABLED configuration should be set to yes in device config file to enable 4x fast forward support |
| 5 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration should be set as yes/no in device config file for SOC level playback verification (default: no) |
| 6 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration should be set to time in seconds for playback duration (default: 10 seconds) |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env and create display for playback environment using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully |
| 2 | Check FastForward 4x Support | Retrieve FIREBOLT_COMPLIANCE_FASTFORWARD_3x_4x_ENABLED configuration value from device config file to verify if 4x fast forward is supported by the device | Configuration value must be retrieved successfully and should be "yes" to proceed with test execution |
| 3 | Execute Fast Forward 4x Test | Retrieve configuration values for AV status check and playback timeout, get H264 29fps stream URL from MediaValidationVariables, construct mediapipeline test command with fastforward4x operation for 10 seconds duration, and execute tdk_mediapipelinetests_trickplay https://&lt;server_hosting_stream&gt;:&lt;port_number&gt;/[H264_29FPS_STREAM_NAME] checkavstatus=no operations=fastforward4x:10 command | Configuration values must be retrieved successfully, stream URL must be obtained correctly, command must be constructed properly, test command execution must start successfully and test application starts execution without errors |
| 4 | Validate Fast Forward 4x Playback | Monitor playback during 4x fast forward operation to verify position progression at accelerated rate, validate smooth frame rendering without excessive frame drops, and ensure no pipeline errors or underflow conditions occur during trick play operation | Fast forward playback at 4x rate must execute smoothly, position must progress at accelerated rate, frame rendering must be stable without errors, and no pipeline failures should occur |
| 5 | Verify Test Completion Status | Check the output from mediapipelinetests execution for success indicators including "Failures: 0" and "Errors: 0" or "failed: 0" status strings to confirm successful test completion | Output must contain success status indicators "Failures: 0" and "Errors: 0" or "failed: 0", confirming successful H264 29fps fast forward 4x playback test execution |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M135