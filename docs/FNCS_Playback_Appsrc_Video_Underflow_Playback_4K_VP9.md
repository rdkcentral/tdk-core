# FNCS_Playback_Appsrc_Video_Underflow_Playback_4K_VP9 Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_288

## TestCase Name
FNCS_Playback_Appsrc_Video_Underflow_Playback_4K_VP9

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To verify playback recovery capability after pushing additional video buffers from "appsrc" once underflow state is reached through playbin and westerossink GStreamer elements. This test validates the media pipeline's resilience to video buffer underflow conditions and its ability to resume normal playback after buffer replenishment, ensuring seamless user experience during video streaming scenarios with temporary network interruptions or buffer depletion.

**VIDEO CODEC:** 4K VP9 (WebM)

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | 4K VP9 WebM video stream must be available and referenced in MediaValidationVariables.video_src_url_webm_4k_vp9 |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 4 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 5 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_USE_VIDEO_SINK configuration in Video_Accelerator.config specifies custom video sink element, currently empty (uses default) |
| 7 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 8 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 10 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 11 | video_src_url_webm_4k_vp9 variable in MediaValidationVariables.py contains 4K VP9 WebM video stream URL for appsrc underflow recovery testing |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env and create display for playback environment using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS config value, get 4K VP9 stream URL from MediaValidationVariables.video_src_url_webm_4k_vp9, construct tdk_mediapipelinetests command with underflow threshold parameter (45061667 bytes), and run test_appsrc_video_underflow with 4K VP9 stream | Configuration values retrieved, 4K VP9 stream URL obtained, command executed: `tdk_mediapipelinetests test_appsrc_video_underflow <4K_VP9_STREAM_URL> checkavstatus=no validateFullPlayback underflow_threshold=45061667`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline with Appsrc | Initialize playbin element and configure with force_appsrc flag for video-only playback, set video_underflow_test flag to enable underflow recovery testing | Playbin element created successfully with appsrc integration and video underflow recovery testing capability enabled |
| 4 | Configure Video Output | Create westerossink element and link it to playbin with video underflow signal connection for monitoring buffer state | Westerossink element created and linked successfully to playbin with underflow callback configured |
| 5 | Setup Appsrc Element | Configure appsrc with size property set to underflow threshold (45061667 bytes), set appropriate 4K VP9 WebM video caps, and connect push-buffer signal for manual feeding | Appsrc element configured successfully with threshold size and 4K VP9 WebM video capabilities |
| 6 | Start Pipeline and Feed Initial Buffers | Set pipeline to PLAYING state and begin feeding video data through appsrc up to threshold limit | Pipeline transitions to PLAYING state successfully and starts consuming video buffers from appsrc |
| 7 | Reach Buffer Threshold | Continue feeding video buffers via appsrc until threshold bytes (45061667) are reached, triggering initial playback | Threshold limit reached successfully, pipeline consuming all provided video buffer data and displaying video frames |
| 8 | Trigger Buffer Underflow | Emit end-of-stream signal from appsrc to stop buffer feeding and trigger video underflow condition | End-of-stream signal emitted successfully, causing pipeline to enter video underflow state |
| 9 | Detect Underflow Signal | Monitor westerossink buffer-underflow-callback signal to capture video underflow event detection and confirm underflow state | Video buffer underflow signal received successfully indicating proper underflow detection mechanism |
| 10 | Pause Pipeline for Buffer Replenishment | Set pipeline to PAUSED state upon underflow signal detection to prepare for additional buffer feeding | Pipeline transitions to PAUSED state successfully, maintaining current playback position |
| 11 | Feed Additional Video Buffers | Push additional video buffers (double the threshold amount) through appsrc to replenish buffer queue for playback recovery | Additional video buffers (90123334 bytes) fed successfully through appsrc, replenishing pipeline buffer queue |
| 12 | Resume Playback from Expected Position | Set pipeline back to PLAYING state and verify playback continues from expected position without frame drops or artifacts | Pipeline transitions to PLAYING state successfully, video playback resumes from correct position without visual artifacts |
| 13 | Monitor Continuous Playback | Verify continuous video playback for configured duration to ensure stable recovery from underflow condition | Video playback continues smoothly without interruptions, demonstrating successful underflow recovery |
| 14 | Validate Pipeline Performance | Monitor video frame rate, PTS timestamps, and overall playback quality during recovery process | Video frame rate maintained, PTS timestamps consistent, playback quality preserved throughout recovery |
| 15 | Complete Recovery Test | Allow test to run for full duration to validate long-term stability of underflow recovery mechanism | Test completes full duration successfully, confirming robust underflow recovery capability |
| 16 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating 4K VP9 appsrc video underflow recovery completed without errors |
| 17 | Cleanup Pipeline | Set playbin pipeline to NULL state and release resources | Pipeline transitions to NULL state successfully and resources cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 7 minutes  

**Priority:** High

**Release Version:** M130