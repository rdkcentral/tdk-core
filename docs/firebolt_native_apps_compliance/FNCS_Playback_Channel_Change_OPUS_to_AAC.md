# FNCS_Playback_Channel_Change_OPUS_to_AAC Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_190

## TestCase Name
FNCS_Playback_Channel_Change_OPUS_to_AAC

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To test channel change functionality from a OPUS stream to AAC stream through playbin gst element and westerossink, validating the media pipeline's capability to seamlessly switch between different audio codecs during channel change operations.

**VIDEO CODEC:** OPUS to AAC

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | OPUS stream must be available and referenced in MediaValidationVariables.video_src_url_opus (DASH_VP9_OPUS_WebM/master.mpd) |
| 3 | AAC stream must be available and referenced in MediaValidationVariables.video_src_url_aac (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd) |
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
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_SECOND_CHANNEL_TIMEOUT config values, get OPUS stream URL from MediaValidationVariables.video_src_url_opus (DASH_VP9_OPUS_WebM/master.mpd) and AAC stream URL from MediaValidationVariables.video_src_url_aac (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd), construct tdk_mediapipelinetests command, and run test_channel_change_playback with both streams | Configuration values retrieved, stream URLs obtained, command executed: `tdk_mediapipelinetests test_channel_change_playback <DASH_VP9_OPUS_WebM/master.mpd> <DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd> checkavstatus=no timeout=<TIMEOUT1>,<TIMEOUT2>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for multi-codec channel change playback, configure westeros-sink for video rendering with audio codec switching capabilities | Playbin element created successfully with channel change support, westeros-sink configured with adaptive audio codec processing enabled |
| 4 | Start OPUS Playback | Begin playback with OPUS stream as first channel, monitor for proper OPUS audio decoding and VP9 video processing | OPUS playback starts successfully with proper OPUS audio codec decoding, VP9 video processing, and WebM container support |
| 5 | Monitor First Channel | Continue monitoring OPUS stream playback for the configured first channel timeout duration, validate OPUS audio codec performance and DASH streaming stability | First channel playback proceeds normally for specified timeout duration, OPUS audio frames processed correctly with stable WebM streaming |
| 6 | Initiate Channel Change | Execute channel change operation from OPUS stream to AAC stream, monitor pipeline state transition during audio codec and video codec switching | Channel change operation initiated successfully, pipeline transitions smoothly from OPUS/VP9 to AAC/H264 without decoder errors |
| 7 | Validate Audio and Video Codec Transition | Verify seamless transition from OPUS audio codec to AAC audio codec and VP9 video codec to H264 video codec, confirm codec adaptation without playback interruption | Codec transition completed successfully, pipeline switches from OPUS/VP9 decoders to AAC/H264 decoders with proper audio and video codec adaptation |
| 8 | Start AAC Playback | Begin playback with AAC stream as second channel, monitor for proper AAC audio quality and H264 video codec performance | AAC playback starts successfully after channel change with proper audio quality and H264 video codec functionality |
| 9 | Monitor Second Channel | Continue monitoring AAC stream playback for the configured second channel timeout duration, validate AAC audio codec performance and streaming stability | Second channel playback proceeds normally for specified timeout duration, AAC audio frames processed correctly with stable H264 video streaming |
| 10 | Validate Channel Change Performance | Verify that channel change operation completed within acceptable time limits and maintained audio/video synchronization throughout audio codec transition | Channel change performance meets expected timing requirements, audio/video synchronization maintained during OPUS to AAC codec transition |
| 11 | Monitor Audio Codec Resources | Track system resource utilization during channel change operation to ensure efficient audio codec switching and decoder management | System resources managed efficiently during audio codec change, audio decoder resources optimized for OPUS to AAC transition |
| 12 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating channel change test completed without errors |
| 13 | Cleanup Pipeline | Set playbin pipeline to NULL state, release both OPUS and AAC stream resources, and clean up audio codec switching components | Pipeline transitions to NULL state successfully, all audio codec resources released, and channel change components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121