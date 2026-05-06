# FNCS_Playback_Channel_Change_HEVC_to_AV1 Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_201

## TestCase Name
FNCS_Playback_Channel_Change_HEVC_to_AV1

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To test channel change functionality from a HEVC stream to AV1 stream through playbin gst element and westerossink, validating the media pipeline's capability to seamlessly switch between different advanced video codecs during channel change operations.

**VIDEO CODEC:** HEVC to AV1

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | HEVC stream must be available and referenced in MediaValidationVariables.video_src_url_hevc (DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd) |
| 3 | AV1 stream must be available and referenced in MediaValidationVariables.video_src_url_av1 (TDK_Asset_DASH_AV1_AAC/master.mpd) |
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
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_SECOND_CHANNEL_TIMEOUT config values, get HEVC stream URL from MediaValidationVariables.video_src_url_hevc (DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd) and AV1 stream URL from MediaValidationVariables.video_src_url_av1 (TDK_Asset_DASH_AV1_AAC/master.mpd), construct tdk_mediapipelinetests command, and run test_channel_change_playback with both streams | Configuration values retrieved, stream URLs obtained, command executed: `tdk_mediapipelinetests test_channel_change_playback <DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd> <TDK_Asset_DASH_AV1_AAC/master.mpd> checkavstatus=no timeout=<TIMEOUT1>,<TIMEOUT2>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for advanced codec channel change playback, configure westeros-sink for video rendering with next-generation codec switching capabilities | Playbin element created successfully with channel change support, westeros-sink configured with advanced codec processing enabled |
| 4 | Start HEVC Playback | Begin playback with HEVC stream as first channel, monitor for proper HEVC video decoding and high-efficiency codec performance | HEVC playback starts successfully with proper HEVC codec decoding, video quality, and high-efficiency compression performance |
| 5 | Monitor First Channel | Continue monitoring HEVC stream playback for the configured first channel timeout duration, validate HEVC codec performance and DASH streaming protocol | First channel playback proceeds normally for specified timeout duration, HEVC frames processed correctly with efficient codec performance |
| 6 | Initiate Channel Change | Execute channel change operation from HEVC stream to AV1 stream, monitor pipeline state transition during advanced codec switching | Channel change operation initiated successfully, pipeline transitions smoothly from HEVC to AV1 codec without decoder errors |
| 7 | Validate Advanced Codec Transition | Verify seamless transition from HEVC codec to AV1 codec, confirm next-generation codec adaptation and switching without playback interruption | Advanced codec transition completed successfully, pipeline switches from HEVC to AV1 decoder with proper next-generation codec adaptation |
| 8 | Start AV1 Playback | Begin playback with AV1 stream as second channel, monitor for proper AV1 video quality and next-generation codec performance | AV1 playback starts successfully after channel change with proper video quality and AV1 next-generation codec functionality |
| 9 | Monitor Second Channel | Continue monitoring AV1 stream playback for the configured second channel timeout duration, validate AV1 codec performance and streaming stability | Second channel playback proceeds normally for specified timeout duration, AV1 frames processed correctly with advanced codec efficiency |
| 10 | Validate Channel Change Performance | Verify that channel change operation completed within acceptable time limits and maintained audio/video synchronization throughout advanced codec transition | Channel change performance meets expected timing requirements, audio/video synchronization maintained during HEVC to AV1 codec transition |
| 11 | Monitor Advanced Codec Resources | Track system resource utilization during channel change operation to ensure efficient advanced codec switching and decoder management | System resources managed efficiently during advanced codec change, decoder resources optimized for HEVC to AV1 transition |
| 12 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating channel change test completed without errors |
| 13 | Cleanup Pipeline | Set playbin pipeline to NULL state, release both HEVC and AV1 stream resources, and clean up advanced codec switching components | Pipeline transitions to NULL state successfully, all advanced codec resources released, and channel change components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121