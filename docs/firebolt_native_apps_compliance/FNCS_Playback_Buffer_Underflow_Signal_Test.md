# FNCS_Playback_Buffer_Underflow_Signal_Test Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_148

## TestCase Name
FNCS_Playback_Buffer_Underflow_Signal_Test

## Table Of Contents
- [FNCS\_Playback\_Buffer\_Underflow\_Signal\_Test Test Case Documentation](#fncs_playback_buffer_underflow_signal_test-test-case-documentation)
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Table Of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To test if buffer underflow callback is received upon video underrun from westerossink, validating the media pipeline's capability to properly detect and signal buffer underflow conditions when video content becomes unavailable due to buffer underrun situations.

**VIDEO CODEC:** H264

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | Video underflow stream must be available and referenced in MediaValidationVariables.video_src_url_underflow_stream (TDK_Asset_Sunrise_underflow_stream_v2.mp4) |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 4 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 5 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_USE_VIDEO_SINK configuration in Video_Accelerator.config specifies custom video sink element, currently empty (uses default) |
| 7 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 8 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 10 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 11 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration in Video_Accelerator.config specifies playback duration in seconds before checking for AV playback |
| 12 | FIREBOLT_COMPLIANCE_UNDERFLOW_VIDEO_END_POINT configuration in Video_Accelerator.config specifies the point where video underrun occurs and buffer underflow signal should be detected |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env and create display for playback environment using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_UNDERFLOW_VIDEO_END_POINT config values, get underflow stream URL from MediaValidationVariables.video_src_url_underflow_stream, construct tdk_mediapipelinetests command, and run test_buffer_underflow_signal with underflow stream | Configuration values retrieved, underflow stream URL obtained, command executed: `tdk_mediapipelinetests test_buffer_underflow_signal <UNDERFLOW_STREAM_URL> checkavstatus=no timeout=<TIMEOUT> videoEnd=<END_POINT>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for underflow stream playback, configure westeros-sink for video rendering with buffer monitoring capabilities | Playbin element created successfully with underflow stream support, westeros-sink configured with buffer monitoring enabled |
| 4 | Start Normal AV Playback | Begin synchronized audio and video playback with normal buffer levels, monitor for proper synchronization and quality | Normal AV playback starts successfully with proper audio and video synchronization and quality |
| 5 | Monitor Playback Progress | Continue monitoring audio and video playback until reaching the configured video end point where video buffer underflow is expected to occur | Playback proceeds normally until video end point, both audio and video frames processed correctly |
| 6 | Detect Video Buffer Underflow | Wait for video buffer underflow condition at the configured video end point where video data becomes unavailable | Video buffer underflow condition detected successfully at expected video end point when video buffer depletes |
| 7 | Monitor Westeros-Sink Signal | Monitor westeros-sink component for buffer-underflow-callback signal emission when video underrun occurs | Westeros-sink emits buffer underflow signal successfully indicating proper underflow detection mechanism |
| 8 | Capture Underflow Signal | Capture and validate the buffer underflow callback signal from westeros-sink to confirm proper underflow notification | Buffer underflow signal captured successfully from westeros-sink component with correct timing and signal parameters |
| 9 | Continue Signal Monitoring | Continue monitoring for the complete duration of the configured timeout to ensure signal persistence and stability | Signal monitoring continues for full timeout duration without unexpected signal interruptions or false positives |
| 10 | Validate Signal Reception | Verify that the buffer underflow signal was properly received and processed by the media pipeline framework | Buffer underflow signal received and processed correctly by media pipeline framework with proper signal handling |
| 11 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating buffer underflow signal test completed without errors |
| 12 | Cleanup Pipeline | Set playbin pipeline to NULL state, release underflow stream resources, and clean up buffer monitoring components | Pipeline transitions to NULL state successfully, underflow stream resources released, and buffer monitoring components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121