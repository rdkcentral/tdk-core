# FNCS_Playback_Appsrc_Video_Underflow_Signal_HEVC Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_247

## TestCase Name
FNCS_Playback_Appsrc_Video_Underflow_Signal_HEVC

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To verify if underflow signal is captured by westerossink after reaching the amount of buffers pushed by "appsrc" element to pipeline created via "playbin" and "westerossink" GStreamer elements. This test validates the media pipeline's capability to detect video buffer underflow conditions by monitoring underflow signals without attempting playback recovery, focusing specifically on signal detection and validation using appsrc for controlled video buffer feeding with deliberate buffer starvation to trigger underflow events.

**VIDEO CODEC:** HEVC (30fps)

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | HEVC video stream (30fps) must be available and referenced in MediaValidationVariables.video_src_url_hevc_30fps |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 4 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 5 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_USE_VIDEO_SINK configuration in Video_Accelerator.config specifies custom video sink element, currently empty (uses default) |
| 7 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 8 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 10 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 11 | video_src_url_hevc_30fps variable in MediaValidationVariables.py contains HEVC video stream URL (30fps) for appsrc underflow signal testing |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS config value, get HEVC stream URL from MediaValidationVariables.video_src_url_hevc_30fps, construct tdk_mediapipelinetests command with underflow threshold parameter (1290444 bytes), and run test_appsrc_video_underflow_signal with HEVC stream | Configuration values retrieved, HEVC stream URL obtained, command executed: `tdk_mediapipelinetests test_appsrc_video_underflow_signal <HEVC_STREAM_URL> checkavstatus=no validateFullPlayback underflow_threshold=1290444`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline with Appsrc | Initialize playbin element and configure with force_appsrc flag for video-only playback, set video_underflow_test and checkSignalTest flags to enable underflow signal detection | Playbin element created successfully with appsrc integration and video underflow signal testing capability enabled |
| 4 | Configure Video Output | Create westerossink element and link it to playbin with video underflow signal connection for monitoring buffer state | Westerossink element created and linked successfully to playbin with underflow callback configured |
| 5 | Setup Appsrc Element | Configure appsrc with size property set to underflow threshold (1290444 bytes), set appropriate HEVC video caps, and connect push-buffer signal for manual feeding | Appsrc element configured successfully with threshold size and HEVC video capabilities |
| 6 | Start Pipeline and Feed Buffers | Set pipeline to PLAYING state and begin feeding video data through appsrc up to threshold limit | Pipeline transitions to PLAYING state successfully and starts consuming video buffers from appsrc |
| 7 | Reach Buffer Threshold | Continue feeding video buffers via appsrc until threshold bytes (1290444) are reached | Threshold limit reached successfully, pipeline consuming all provided video buffer data |
| 8 | Trigger Buffer Underflow | Emit end-of-stream signal from appsrc to stop buffer feeding and trigger video underflow condition | End-of-stream signal emitted successfully, causing pipeline to enter video underflow state |
| 9 | Detect Underflow Signal | Monitor westerossink buffer-underflow-callback signal to capture video underflow event detection | Video buffer underflow signal received successfully indicating proper underflow detection mechanism |
| 10 | Complete Signal Test | Exit test immediately after underflow signal detection without attempting playback recovery since checkSignalTest flag is enabled | Test completes successfully after confirming underflow signal detection |
| 11 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating HEVC appsrc video underflow signal detection completed without errors |
| 12 | Cleanup Pipeline | Set playbin pipeline to NULL state and release resources | Pipeline transitions to NULL state successfully and resources cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator, RDKTV

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M122