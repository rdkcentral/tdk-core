# FNCS Playback FastForward 2x H264 24Fps Test Documentation

## TestCase ID
FNCS_PLAYBACK_238

## TestCase Name
FNCS_Playback_FastForward_2x_H264_24Fps

## Table Of Contents
1. [TestCase ID](#testcase-id)
2. [TestCase Name](#testcase-name)
3. [Objective](#objective)
4. [Preconditions](#preconditions)
5. [Test Steps](#test-steps)
6. [Test Attributes](#test-attributes)

## Objective

This test validates the fast forward functionality of H264 DASH video streams at 24fps playback rate using GStreamer pipeline. The test verifies that the media pipeline can successfully handle trick play operations specifically for H264 codec streams with 24fps cinematic frame rate, ensuring proper playback rate manipulation and video stream processing.

**VIDEO CODEC:** H264

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | TDK_FNCS_Package should be installed in DUT |
| 2 | TDK_Asset_H264_DASH_24FPS_Stream must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration should be set as no (default) in Video_Accelerator.config to control whether SOC level audio/video playback verification should be performed during test execution |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration should be set to 10 seconds (default) in Video_Accelerator.config to specify the duration for which media playback should continue before test completion |
| 5 | video_src_url_dash_h264_24fps variable must be configured with TDK_Asset_H264_DASH_24FPS_Stream in MediaValidationVariables.py as URL or file path for the H264 24fps DASH video test stream used for fast forward validation |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env and create display for playback environment using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS config value, get H264 24fps DASH stream URL from MediaValidationVariables.video_src_url_dash_h264_24fps, construct tdk_mediapipelinetests command with fastforward2x operation, and run test_trickplay with H264 24fps stream | Configuration values retrieved, H264 24fps stream URL obtained, command executed: `tdk_mediapipelinetests_trickplay https://<server_hosting_stream>:<port_number>/TDK_Asset_H264_DASH_24FPS_Stream checkavstatus=no operations=fastforward2x:10`, and test application starts execution without errors |
| 3 | Validate H264 24fps Stream Loading | Load and initialize H264 24fps video stream in GStreamer pipeline using playbin element with specified stream URL | H264 24fps stream must be loaded successfully without codec errors and pipeline must transition to READY state |
| 4 | Setup Fast Forward Pipeline | Configure playbin element with rate property set to 2.0 for fast forward operation and setup video sink for H264 24fps stream processing | Pipeline must be configured for 2x fast forward rate and video processing elements must be properly initialized |
| 5 | Execute Fast Forward Playback | Start media playback with 2x fast forward rate for the configured timeout duration and monitor H264 24fps video stream processing during fast forward operation | Fast forward playback must execute smoothly for specified duration with proper H264 24fps stream handling at 2x rate |
| 6 | Validate Playback Completion | Monitor test execution output for completion status and verify that pipeline properly handles fast forward operation without errors | Test must complete within timeout period and return success status indicating proper fast forward functionality |
| 7 | Verify Test Results | Check command output for success indicators including "Failures: 0" and "Errors: 0" or "failed: 0" strings to confirm successful test execution | Output must contain success indicators showing no failures or errors during fast forward H264 24fps playback test |

## Test Attributes

**Supported Models:** Video_Accelerator  
**Estimated Duration:** 3 minutes  
**Priority:** High  
**Release Version:** M121