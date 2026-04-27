# FNCS_Playback_Channel_Change_AV1_to_HEVC Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_200

## TestCase Name
FNCS_Playback_Channel_Change_AV1_to_HEVC

## Table Of Contents
- [FNCS\_Playback\_Channel\_Change\_AV1\_to\_HEVC Test Case Documentation](#fncs_playback_channel_change_av1_to_hevc-test-case-documentation)
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Table Of Contents](#table-of-contents)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To test channel change functionality from an AV1 stream to HEVC stream through playbin gst element and westerossink, validating the media pipeline's capability to seamlessly switch between different video codecs during channel change operations.

**VIDEO CODEC:** AV1 to HEVC

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | AV1 stream must be available and referenced in MediaValidationVariables.video_src_url_av1 (TDK_Asset_DASH_AV1_AAC/master.mpd) |
| 3 | HEVC stream must be available and referenced in MediaValidationVariables.video_src_url_hevc (DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd) |
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
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_SECOND_CHANNEL_TIMEOUT config values, get AV1 stream URL from MediaValidationVariables.video_src_url_av1 (TDK_Asset_DASH_AV1_AAC/master.mpd) and HEVC stream URL from MediaValidationVariables.video_src_url_hevc (DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd), construct tdk_mediapipelinetests command, and run test_channel_change_playback with both streams | Configuration values retrieved, stream URLs obtained, command executed: `tdk_mediapipelinetests test_channel_change_playback <TDK_Asset_DASH_AV1_AAC/master.mpd> <DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd> checkavstatus=no timeout=<TIMEOUT1>,<TIMEOUT2>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for multi-codec channel change playback, configure westeros-sink for video rendering with codec switching capabilities | Playbin element created successfully with channel change support, westeros-sink configured with adaptive codec processing enabled |
| 4 | Start AV1 Playback | Begin playback with AV1 stream as first channel, monitor for proper AV1 video decoding and audio synchronization | AV1 playback starts successfully with proper AV1 codec decoding, video quality, and audio synchronization |
| 5 | Monitor First Channel | Continue monitoring AV1 stream playback for the configured first channel timeout duration, validate AV1 codec performance and DASH streaming protocol | First channel playback proceeds normally for specified timeout duration, AV1 frames processed correctly with stable DASH streaming |
| 6 | Initiate Channel Change | Execute channel change operation from AV1 stream to HEVC stream, monitor pipeline state transition during codec switching | Channel change operation initiated successfully, pipeline transitions smoothly from AV1 to HEVC stream without decoder errors |
| 7 | Validate Codec Transition | Verify seamless transition from AV1 codec to HEVC codec, confirm decoder adaptation and codec switching without playback interruption | Codec transition completed successfully, pipeline switches from AV1 to HEVC decoder with proper codec adaptation and performance |
| 8 | Start HEVC Playback | Begin playback with HEVC stream as second channel, monitor for proper HEVC video quality and codec performance | HEVC playback starts successfully after channel change with proper video quality and HEVC codec functionality |
| 9 | Monitor Second Channel | Continue monitoring HEVC stream playback for the configured second channel timeout duration, validate HEVC codec performance and streaming stability | Second channel playback proceeds normally for specified timeout duration, HEVC frames processed correctly with stable streaming |
| 10 | Validate Channel Change Performance | Verify that channel change operation completed within acceptable time limits and maintained audio/video synchronization throughout codec transition | Channel change performance meets expected timing requirements, audio/video synchronization maintained during codec transition |
| 11 | Monitor Codec Resources | Track system resource utilization during channel change operation to ensure efficient codec switching and memory management | System resources managed efficiently during codec change, decoder resources optimized for AV1 to HEVC transition |
| 12 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating channel change test completed without errors |
| 13 | Cleanup Pipeline | Set playbin pipeline to NULL state, release both AV1 and HEVC stream resources, and clean up codec switching components | Pipeline transitions to NULL state successfully, all codec resources released, and channel change components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121