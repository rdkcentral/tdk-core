# FNCS_Playback_Channel_Change_HD_to_SD Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_194

## TestCase Name
FNCS_Playback_Channel_Change_HD_to_SD

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To test channel change functionality from a HD stream to SD stream through playbin gst element and westerossink, validating the media pipeline's capability to seamlessly switch between different resolutions during channel change operations.

**VIDEO CODEC:** HD to SD Resolution

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | HD stream must be available and referenced in MediaValidationVariables.video_src_url_mp4_1080p (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_1080p.mp4) |
| 3 | SD stream must be available and referenced in MediaValidationVariables.video_src_url_mp4_360p (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_360p.mp4) |
| 4 | FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration in Video_Accelerator.config enables/disables SOC-level audio/video playback verification check, currently set to no |
| 5 | FIREBOLT_COMPLIANCE_CHECK_PTS configuration in Video_Accelerator.config enables/disables video PTS timestamp validation during playback, currently set to yes |
| 6 | FIREBOLT_COMPLIANCE_CHECK_FPS configuration in Video_Accelerator.config enables/disables video frame rate validation during playback, currently set to yes |
| 7 | FIREBOLT_COMPLIANCE_USE_VIDEO_SINK configuration in Video_Accelerator.config specifies custom video sink element, currently empty (uses default) |
| 8 | FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration in Video_Accelerator.config enables millisecond-level playback position validation, currently set to yes |
| 9 | FIREBOLT_COMPLIANCE_USE_APPSRC configuration in Video_Accelerator.config enables/disables appsrc usage in pipeline instead of direct URI, currently set to yes |
| 10 | FIREBOLT_COMPLIANCE_START_WESTEROS configuration in Video_Accelerator.config enables/disables automatic westeros compositor startup, currently set to no |
| 11 | FIREBOLT_COMPLIANCE_CHECK_AUDIO configuration in Video_Accelerator.config enables/disables audio frame rate validation during playback, currently set to yes |
| 12 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT configuration in Video_Accelerator.config specifies playback duration in seconds for first channel |
| 13 | FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_SECOND_CHANNEL_TIMEOUT configuration in Video_Accelerator.config specifies playback duration in seconds for second channel after channel change |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|----------------|
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env. Check if RDKWindowManager is present. If RDKWindowManager is present, create display for playback environment using RDKWindowManager. Otherwise, create display using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully using either RDKWindowManager (if present) or RDKShell/westeros |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_SECOND_CHANNEL_TIMEOUT config values, get HD stream URL from MediaValidationVariables.video_src_url_mp4_1080p (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_1080p.mp4) and SD stream URL from MediaValidationVariables.video_src_url_mp4_360p (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_360p.mp4), construct tdk_mediapipelinetests command, and run test_channel_change_playback with both streams | Configuration values retrieved, stream URLs obtained, command executed: `tdk_mediapipelinetests test_channel_change_playback <DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_1080p.mp4> <DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_360p.mp4> checkavstatus=no timeout=<TIMEOUT1>,<TIMEOUT2> checkAudioFPS=no`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for multi-resolution channel change playback, configure westeros-sink for video rendering with resolution scaling capabilities | Playbin element created successfully with channel change support, westeros-sink configured with adaptive resolution processing enabled |
| 4 | Start HD Playback | Begin playback with HD 1080p stream as first channel, monitor for proper high-definition video quality and H264 decoding | HD 1080p playback starts successfully with proper high-definition video quality, H264 codec decoding, and AAC audio processing |
| 5 | Monitor First Channel | Continue monitoring HD 1080p stream playback for the configured first channel timeout duration, validate HD resolution performance and streaming stability | First channel playback proceeds normally for specified timeout duration, HD 1080p frames processed correctly with stable high-resolution streaming |
| 6 | Initiate Channel Change | Execute channel change operation from HD 1080p stream to SD 360p stream, monitor pipeline state transition during resolution downscaling | Channel change operation initiated successfully, pipeline transitions smoothly from HD to SD resolution without decoder errors |
| 7 | Validate Resolution Transition | Verify seamless transition from HD 1080p to SD 360p format, confirm resolution downscaling without playback interruption | Resolution transition completed successfully, pipeline switches from HD 1080p to SD 360p with proper resolution downscaling and video quality adaptation |
| 8 | Start SD Playback | Begin playback with SD 360p stream as second channel, monitor for proper standard-definition video quality and codec performance | SD 360p playback starts successfully after channel change with proper standard-definition video quality and H264 codec functionality |
| 9 | Monitor Second Channel | Continue monitoring SD 360p stream playback for the configured second channel timeout duration, validate SD resolution performance and streaming stability | Second channel playback proceeds normally for specified timeout duration, SD 360p frames processed correctly with stable standard-definition streaming |
| 10 | Validate Channel Change Performance | Verify that channel change operation completed within acceptable time limits and maintained audio/video synchronization throughout resolution transition | Channel change performance meets expected timing requirements, audio/video synchronization maintained during resolution downscaling transition |
| 11 | Monitor Resource Optimization | Track system resource utilization during channel change operation to ensure efficient memory management for resolution downscaling | System resources optimized efficiently during resolution downscaling, video memory usage reduced appropriately for HD to SD transition |
| 12 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating channel change test completed without errors |
| 13 | Cleanup Pipeline | Set playbin pipeline to NULL state, release both HD and SD stream resources, and clean up resolution scaling components | Pipeline transitions to NULL state successfully, all stream resources released, and channel change components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121