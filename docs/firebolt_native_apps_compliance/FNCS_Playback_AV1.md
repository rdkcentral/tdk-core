# FNCS_Playback_AV1 Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_04

## TestCase Name
FNCS_Playback_AV1

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Table Of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To test the video playback of AV1 stream through 'playbin' and 'westerossink' GStreamer elements, validating the media pipeline's capability to properly handle AV1 video codec decoding and playback functionality with high efficiency compression standards.

**VIDEO CODEC:** AV1

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | AV1 stream must be available and referenced in MediaValidationVariables.video_src_url_av1 (TDK_Asset_DASH_AV1_AAC/master.mpd) |
| 3 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 4 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 5 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_USE_VIDEO_SINK configuration in Video_Accelerator.config specifies custom video sink element, currently empty (uses default) |
| 7 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 8 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 10 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 11 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration in Video_Accelerator.config specifies playback duration in seconds, default 10 seconds |
| 12 | video_src_url_av1 variable in MediaValidationVariables.py contains AV1 stream URL (TDK_Asset_DASH_AV1_AAC/master.mpd) for playback testing |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT config values, get AV1 stream URL from MediaValidationVariables.video_src_url_av1, construct tdk_mediapipelinetests command, and run test_generic_playback with AV1 stream | Configuration values retrieved, AV1 stream URL obtained, command executed: `tdk_mediapipelinetests test_generic_playback <AV1_STREAM_URL> checkavstatus=no timeout=10`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element and configure for AV1 video stream playback, enable AV1 decoder and establish video processing pipeline with westerossink | Playbin element created successfully with AV1 video stream support and AV1 decoder configured |
| 4 | Configure AV1 Video Output | Create and configure video sink element for AV1 video playback, establish video rendering with hardware acceleration if available | Video sink element configured successfully for AV1 playback with proper video rendering pipeline |
| 5 | Start AV1 Video Playback | Set pipeline to PLAYING state and begin playback with AV1 video codec, monitor for video frames and proper decoding | Pipeline transitions to PLAYING state successfully, AV1 video playback starts, and video frame decoding activated |
| 6 | Monitor AV1 Playback Performance | Continuously monitor AV1 video playback for configured timeout duration (default 10 seconds), verify video frame processing and decode performance | AV1 video playback proceeds successfully for full timeout duration with stable video frames and efficient decode performance |
| 7 | Validate Video Quality | Verify AV1 video decoding quality and frame consistency during playback, ensure no corruption or visual artifacts | AV1 video displays correctly with high quality decoding and no visual artifacts or corruption detected |
| 8 | Monitor Resource Utilization | Track system resource usage during AV1 decoding to ensure efficient processing and proper hardware acceleration usage | System resources utilized efficiently with appropriate hardware acceleration for AV1 decoding |
| 9 | Complete Playback Cycle | Allow AV1 video playback to continue for full configured duration, monitor for consistent performance throughout | AV1 video playback completes successfully for entire duration with consistent decode performance |
| 10 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating AV1 video playback completed without errors |
| 11 | Cleanup Pipeline | Set playbin pipeline to NULL state, release AV1 video resources, and clean up video processing components | Pipeline transitions to NULL state successfully, AV1 video resources released, and video components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121
