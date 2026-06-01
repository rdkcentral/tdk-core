# FNCS_Playback_Buffer_Underflow_Playback_Test Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_147

## TestCase Name
FNCS_Playback_Buffer_Underflow_Playback_Test

## Table Of Contents
- [FNCS\_Playback\_Buffer\_Underflow\_Playback\_Test Test Case Documentation](#fncs_playback_buffer_underflow_playback_test-test-case-documentation)
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Table Of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To verify that buffer underflow signal is received upon video underrun and validate the media pipeline's capability to fill the video buffer by seeking to the video start point and verify playback recovery is as expected, ensuring proper handling of buffer underflow conditions and seamless playback recovery.

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
| 12 | FIREBOLT_COMPLIANCE_VIDEO_END_POINT configuration in Video_Accelerator.config specifies the point where video underrun occurs |
| 13 | FIREBOLT_COMPLIANCE_VIDEO_START_POINT configuration in Video_Accelerator.config specifies the point where video playback resumes after underrun recovery |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, FIREBOLT_COMPLIANCE_VIDEO_END_POINT, and FIREBOLT_COMPLIANCE_VIDEO_START_POINT config values, get underflow stream URL from MediaValidationVariables.video_src_url_underflow_stream, construct tdk_mediapipelinetests command, and run test_buffer_underflow_playback with underflow stream | Configuration values retrieved, underflow stream URL obtained, command executed: `tdk_mediapipelinetests test_buffer_underflow_playback <UNDERFLOW_STREAM_URL> checkavstatus=no timeout=<TIMEOUT> videoEnd=<END_POINT> videoStart=<START_POINT>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for underflow stream playback, configure video and audio processing with buffer monitoring capabilities | Playbin element created successfully with underflow stream support and buffer monitoring enabled |
| 4 | Start Normal Playback | Begin video playback with normal buffer levels, monitor for proper audio and video synchronization | Normal playback starts successfully with proper audio and video synchronization |
| 5 | Monitor Playback Progress | Continue playback monitoring until reaching the configured video end point where underflow is expected to occur | Playback proceeds normally until video end point, audio and video frames processed correctly |
| 6 | Detect Buffer Underflow | Wait for buffer underflow signal at the configured video end point where video data becomes unavailable while audio continues | Buffer underflow signal received successfully at expected video end point, audio playback continues while video buffer depletes |
| 7 | Validate Underflow Condition | Verify that video playback stops while audio continues, confirm buffer underflow signal is properly detected and handled | Video playback stops as expected while audio continues, buffer underflow condition properly detected and signaled |
| 8 | Pause Pipeline | Pause the media pipeline after buffer underflow detection to prepare for recovery operation | Pipeline paused successfully after underflow detection, ready for recovery operation |
| 9 | Seek to Recovery Point | Execute seek operation to the configured video start point to refill the video buffer and resume normal playback | Seek operation executed successfully to video start point, video buffer refill initiated |
| 10 | Resume Playback | Resume pipeline playback from the seek position with refilled video buffer, monitor for proper recovery | Pipeline resumed successfully from seek position, video buffer refilled and normal playback restored |
| 11 | Validate Recovery Playback | Verify that video and audio playback resume normally after buffer recovery, confirm proper synchronization and quality | Video and audio playback resume normally with proper synchronization, buffer underflow condition resolved successfully |
| 12 | Monitor Continued Playback | Continue monitoring playback for configured timeout duration to ensure stable operation after recovery | Continued playback proceeds stably for full timeout duration without additional underflow conditions |
| 13 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating buffer underflow playback recovery completed without errors |
| 14 | Cleanup Pipeline | Set playbin pipeline to NULL state, release underflow stream resources, and clean up buffer monitoring components | Pipeline transitions to NULL state successfully, underflow stream resources released, and buffer monitoring components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121