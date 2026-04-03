# FNCS_Playback_Channel_Change_SD_to_HD Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_195

## TestCase Name
FNCS_Playback_Channel_Change_SD_to_HD

## Table Of Contents
- [FNCS\_Playback\_Channel\_Change\_SD\_to\_HD Test Case Documentation](#fncs_playback_channel_change_sd_to_hd-test-case-documentation)
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Table Of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To test channel change functionality from a SD stream to HD stream through playbin gst element and westerossink, validating the media pipeline's capability to seamlessly switch between different video resolutions during channel change operations.

**VIDEO CODEC:** SD to HD Resolution Change

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | SD stream must be available and referenced in MediaValidationVariables.video_src_url_mp4_360p (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_360p.mp4) |
| 3 | HD stream must be available and referenced in MediaValidationVariables.video_src_url_mp4_1080p (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_1080p.mp4) |
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
| 1 | Initialize Test Environment | Setup environment for playback using platform specific environment variables from TDK.env and create display for playback environment using RDKShell plugin or using westeros --renderer command | All environment variables must be set successfully and display for playback must be created successfully |
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_SECOND_CHANNEL_TIMEOUT config values, get SD stream URL from MediaValidationVariables.video_src_url_mp4_360p (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_360p.mp4) and HD stream URL from MediaValidationVariables.video_src_url_mp4_1080p (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_1080p.mp4), construct tdk_mediapipelinetests command, and run test_channel_change_playback with both streams | Configuration values retrieved, stream URLs obtained, command executed: `tdk_mediapipelinetests test_channel_change_playback <DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_360p.mp4> <DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_1080p.mp4> checkavstatus=no timeout=<TIMEOUT1>,<TIMEOUT2>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for resolution scaling channel change playback, configure westeros-sink for video rendering with adaptive resolution support | Playbin element created successfully with resolution scaling support, westeros-sink configured with adaptive video resolution processing enabled |
| 4 | Start SD Playback | Begin playbook with SD stream (360p) as first channel, monitor for proper 360p video decoding and H264 codec performance | SD playback starts successfully with proper 360p video resolution, H264 codec decoding, and AAC audio processing |
| 5 | Monitor First Channel | Continue monitoring SD stream playback for the configured first channel timeout duration, validate 360p resolution performance and streaming stability | First channel playback proceeds normally for specified timeout duration, 360p video frames processed correctly with stable H264 streaming |
| 6 | Initiate Channel Change | Execute channel change operation from SD stream (360p) to HD stream (1080p), monitor pipeline state transition during resolution scaling | Channel change operation initiated successfully, pipeline transitions smoothly from 360p to 1080p resolution without decoder errors |
| 7 | Validate Resolution Transition | Verify seamless transition from 360p resolution to 1080p resolution, confirm video resolution adaptation without playback interruption | Resolution transition completed successfully, pipeline switches from 360p to 1080p decoder configuration with proper resolution scaling adaptation |
| 8 | Start HD Playback | Begin playback with HD stream (1080p) as second channel, monitor for proper 1080p video quality and H264 codec performance at higher resolution | HD playback starts successfully after channel change with proper 1080p video quality and H264 codec functionality at higher bitrate |
| 9 | Monitor Second Channel | Continue monitoring HD stream playback for the configured second channel timeout duration, validate 1080p resolution performance and streaming stability | Second channel playback proceeds normally for specified timeout duration, 1080p video frames processed correctly with stable high-resolution H264 streaming |
| 10 | Validate Channel Change Performance | Verify that channel change operation completed within acceptable time limits and maintained audio/video synchronization throughout resolution transition | Channel change performance meets expected timing requirements, audio/video synchronization maintained during 360p to 1080p resolution transition |
| 11 | Monitor Video Resolution Resources | Track system resource utilization during resolution scaling to ensure efficient video decoder management and memory allocation | System resources managed efficiently during resolution change, video decoder resources optimized for SD to HD transition |
| 12 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating channel change test completed without errors |
| 13 | Cleanup Pipeline | Set playbin pipeline to NULL state, release both SD and HD stream resources, and clean up resolution scaling components | Pipeline transitions to NULL state successfully, all resolution scaling resources released, and channel change components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121