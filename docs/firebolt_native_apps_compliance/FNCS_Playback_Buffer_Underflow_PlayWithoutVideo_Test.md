# FNCS_Playback_Buffer_Underflow_PlayWithoutVideo_Test Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_146

## TestCase Name
FNCS_Playback_Buffer_Underflow_PlayWithoutVideo_Test

## Table Of Contents
- [FNCS\_Playback\_Buffer\_Underflow\_PlayWithoutVideo\_Test Test Case Documentation](#fncs_playback_buffer_underflow_playwithoutvideo_test-test-case-documentation)
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Table Of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To verify that only audio continues to play when the video buffer is empty during buffer underflow conditions, validating the media pipeline's capability to maintain audio playback continuity while video content becomes unavailable due to buffer underrun situations.

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
| 12 | FIREBOLT_COMPLIANCE_VIDEO_END_POINT configuration in Video_Accelerator.config specifies the point where video underrun occurs and only audio should continue |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env and create display for playback environment using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_VIDEO_END_POINT config values, get underflow stream URL from MediaValidationVariables.video_src_url_underflow_stream, construct tdk_mediapipelinetests command, and run test_buffer_underflow_playback_test with underflow stream | Configuration values retrieved, underflow stream URL obtained, command executed: `tdk_mediapipelinetests test_buffer_underflow_playback_test <UNDERFLOW_STREAM_URL> checkavstatus=no timeout=<TIMEOUT> videoEnd=<END_POINT>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for underflow stream playback, configure separate video and audio processing pipelines with buffer monitoring capabilities | Playbin element created successfully with underflow stream support, separate video and audio pipelines configured with buffer monitoring enabled |
| 4 | Start Normal AV Playback | Begin synchronized audio and video playback with normal buffer levels, monitor for proper synchronization and quality | Normal AV playback starts successfully with proper audio and video synchronization and quality |
| 5 | Monitor Playback Progress | Continue monitoring audio and video playback until reaching the configured video end point where video buffer underflow is expected to occur | Playback proceeds normally until video end point, both audio and video frames processed correctly |
| 6 | Detect Video Buffer Underflow | Wait for video buffer underflow condition at the configured video end point where video data becomes unavailable | Video buffer underflow condition detected successfully at expected video end point, video buffer depletes while audio buffer remains available |
| 7 | Verify Video Playback Stops | Confirm that video rendering stops when video buffer becomes empty while maintaining pipeline in PLAYING state | Video rendering stops as expected when buffer empties, pipeline remains in PLAYING state for continued audio processing |
| 8 | Validate Audio Continuity | Verify that audio playback continues uninterrupted despite video buffer underflow, maintain audio quality and synchronization | Audio playback continues uninterrupted with maintained quality, audio frames processed normally despite video underflow |
| 9 | Monitor Audio-Only Playback | Continue monitoring audio-only playback for remaining configured timeout duration to ensure stable audio continuity | Audio-only playback continues stably for remaining timeout duration, consistent audio frame processing without interruption |
| 10 | Verify Pipeline State | Confirm that media pipeline remains in PLAYING state throughout video underflow condition while maintaining audio processing | Pipeline maintains PLAYING state successfully, audio processing continues normally while video pipeline handles underflow gracefully |
| 11 | Validate Buffer Management | Verify proper buffer management where audio buffer remains functional while video buffer underflow is handled appropriately | Buffer management operates correctly, audio buffer maintains functionality while video buffer underflow handled without affecting audio pipeline |
| 12 | Monitor Resource Usage | Track system resource utilization during audio-only playback to ensure efficient operation without video processing overhead | System resources utilized efficiently during audio-only operation, video processing overhead appropriately reduced |
| 13 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating buffer underflow audio continuity test completed without errors |
| 14 | Cleanup Pipeline | Set playbin pipeline to NULL state, release underflow stream resources, and clean up buffer monitoring components | Pipeline transitions to NULL state successfully, underflow stream resources released, and buffer monitoring components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121