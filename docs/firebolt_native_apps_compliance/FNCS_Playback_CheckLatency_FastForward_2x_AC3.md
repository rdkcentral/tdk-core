# FNCS Playback CheckLatency FastForward 2x AC3 Test Documentation

## TestCase ID
FNCS_PLAYBACK_217

## TestCase Name
FNCS_Playback_CheckLatency_FastForward_2x_AC3

## Table Of Contents
1. [TestCase ID](#testcase-id)
2. [TestCase Name](#testcase-name)
3. [Objective](#objective)
4. [Preconditions](#preconditions)
5. [Test Steps](#test-steps)
6. [Test Attributes](#test-attributes)

## Objective

This test validates that the latency observed during AC3 audio fast forward trickplay operations at 2x rate remains within acceptable threshold limits. The test verifies that the media pipeline can successfully handle trick play operations for AC3 codec streams while maintaining low latency performance metrics during fast forward operations.

**AUDIO CODEC:** AC3

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | TDK_FNCS_Package should be installed in DUT |
| 2 | TDK_Asset_AC3_Stream.ac3 must be installed in the server hosting streams or installed inside the device if user is selecting filesrc instead of httpsrc users can configure streams via filesrc (copying stream to USB like file:/tmp/usb/) or httpsrc via HTTPS server (https://<server_hosting_stream>:<port_number>/) based on their setup preference |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration should be set as no (default) in Video_Accelerator.config / RPI-Client.config to control whether SOC level audio/video playback verification should be performed during test execution |
| 4 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration should be set to 10 seconds (default) in Video_Accelerator.config / RPI-Client.config to specify the duration for which media playback should continue before test completion |
| 5 | FIREBOLT_COMPLIANCE_LATENCY_THRESHOLD configuration should be set to 1000 milliseconds (default) in Video_Accelerator.config / RPI-Client.config to specify maximum acceptable latency during trickplay operations |
| 6 | video_src_url_ac3 variable must be configured with TDK_Asset_AC3_Stream.ac3 in MediaValidationVariables.py as URL or file path for the AC3 audio test stream used for latency validation during fast forward |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env and create display for playback environment using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_LATENCY_THRESHOLD config values, get AC3 stream URL from MediaValidationVariables.video_src_url_ac3, construct tdk_mediapipelinetests command with fastforward2x operation and latency checking, and run test_trickplay with AC3 stream | Configuration values retrieved, AC3 stream URL obtained, command executed: `tdk_mediapipelinetests_trickplay https://<server_hosting_stream>:<port_number>/TDK_Asset_AC3_Stream.ac3 checkavstatus=no operations=fastforward2x:10 latency_threshold=1000`, and test application starts execution without errors |
| 3 | Validate AC3 Stream Loading | Load and initialize AC3 audio stream in GStreamer pipeline using playbin element with specified stream URL | AC3 stream must be loaded successfully without codec errors and pipeline must transition to READY state |
| 4 | Setup Fast Forward Pipeline with Latency Monitoring | Configure playbin element with rate property set to 2.0 for fast forward operation, setup audio sink for AC3 stream processing, and enable latency measurement instrumentation | Pipeline must be configured for 2x fast forward rate with latency monitoring enabled and audio processing elements properly initialized |
| 5 | Execute Fast Forward with Latency Measurement | Start media playback with 2x fast forward rate for the configured timeout duration, monitor AC3 audio stream processing during fast forward operation, and continuously measure latency between command input and audio output | Fast forward playback must execute smoothly with AC3 stream handling at 2x rate while latency measurements are continuously recorded |
| 6 | Validate Latency Threshold Compliance | Monitor latency measurements throughout the fast forward operation and verify that all recorded latency values remain below the configured threshold limit | All measured latency values must remain below the threshold limit (default 1000ms) throughout the entire fast forward operation |
| 7 | Verify Test Results | Check command output for success indicators including "Failures: 0" and "Errors: 0" or "failed: 0" strings and confirm latency compliance results | Output must contain success indicators showing no failures or errors and latency measurements within acceptable threshold during fast forward AC3 playback test |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT  
**Estimated Duration:** 3 minutes  
**Priority:** High  
**Release Version:** M121