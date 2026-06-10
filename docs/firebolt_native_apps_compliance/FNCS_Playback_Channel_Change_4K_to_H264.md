# FNCS_Playback_Channel_Change_4K_to_H264 Test Case Documentation

## TestCase ID
FNCS_PLAYBACK_196

## TestCase Name
FNCS_Playback_Channel_Change_4K_to_H264

## Table Of Contents
  - [TestCase ID](#testcase-id)
  - [TestCase Name](#testcase-name)
  - [Objective](#objective)
  - [Preconditions](#preconditions)
  - [Test Steps](#test-steps)
  - [Test Attributes](#test-attributes)

## Objective
To test channel change functionality from a 4K HLS stream to H264 DASH stream through playbin gst element and westerossink, validating the media pipeline's capability to seamlessly switch between different stream formats and resolutions during channel change operations.

**VIDEO CODEC:** 4K HLS to H264

## Preconditions

| ID | Conditions |
|----|------------|
| 1 | tdk_mediapipelinetests application must be installed in DUT |
| 2 | 4K HLS stream must be available and referenced in MediaValidationVariables.video_src_url_4k_hls (HLS_HEVC_AAC/master.m3u8) |
| 3 | H264 DASH stream must be available and referenced in MediaValidationVariables.video_src_url_dash_h264 (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd) |
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
| 2 | Execute Media Pipeline Test | Retrieve FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_TIMEOUT, and FIREBOLT_COMPLIANCE_MEDIAPLAYBACK_SECOND_CHANNEL_TIMEOUT config values, get 4K HLS stream URL from MediaValidationVariables.video_src_url_4k_hls (HLS_HEVC_AAC/master.m3u8) and H264 DASH stream URL from MediaValidationVariables.video_src_url_dash_h264 (DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd), construct tdk_mediapipelinetests command, and run test_channel_change_playback with both streams | Configuration values retrieved, stream URLs obtained, command executed: `tdk_mediapipelinetests test_channel_change_playback <HLS_HEVC_AAC/master.m3u8> <DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd> checkavstatus=no timeout=<TIMEOUT1>,<TIMEOUT2>`, and test application starts execution without errors |
| 3 | Create GStreamer Pipeline | Initialize playbin element for multi-stream channel change playback, configure westeros-sink for video rendering with channel switching capabilities | Playbin element created successfully with channel change support, westeros-sink configured with adaptive streaming enabled |
| 4 | Start 4K HLS Playback | Begin playback with 4K HLS stream as first channel, monitor for proper 4K video and audio synchronization and quality | 4K HLS playback starts successfully with proper high-resolution video and audio synchronization and quality |
| 5 | Monitor First Channel | Continue monitoring 4K HLS stream playback for the configured first channel timeout duration, validate 4K resolution and HLS streaming protocol performance | First channel playback proceeds normally for specified timeout duration, 4K HLS frames processed correctly with proper resolution and streaming stability |
| 6 | Initiate Channel Change | Execute channel change operation from 4K HLS stream to H264 DASH stream, monitor pipeline state transition during stream switching | Channel change operation initiated successfully, pipeline transitions smoothly from 4K HLS to H264 DASH stream without errors |
| 7 | Validate Stream Transition | Verify seamless transition from 4K HLS format to H264 DASH format, confirm resolution change and protocol switching without playback interruption | Stream transition completed successfully, pipeline switches from 4K HLS to H264 DASH format with proper resolution adaptation and protocol change |
| 8 | Start H264 DASH Playback | Begin playback with H264 DASH stream as second channel, monitor for proper H264 video quality and DASH streaming performance | H264 DASH playback starts successfully after channel change with proper video quality and DASH streaming functionality |
| 9 | Monitor Second Channel | Continue monitoring H264 DASH stream playback for the configured second channel timeout duration, validate H264 codec performance and DASH protocol stability | Second channel playback proceeds normally for specified timeout duration, H264 DASH frames processed correctly with stable streaming |
| 10 | Validate Channel Change Performance | Verify that channel change operation completed within acceptable time limits and maintained audio/video synchronization throughout transition | Channel change performance meets expected timing requirements, audio/video synchronization maintained during format and resolution transition |
| 11 | Monitor Resource Management | Track system resource utilization during channel change operation to ensure efficient memory and processing resource management | System resources managed efficiently during channel change, memory usage optimized for stream format transitions |
| 12 | Validate Test Output | Parse tdk_mediapipelinetests output for success indicators "Failures: 0", "Errors: 0", or "failed: 0" | Test output contains success strings indicating channel change test completed without errors |
| 13 | Cleanup Pipeline | Set playbin pipeline to NULL state, release both 4K HLS and H264 DASH stream resources, and clean up channel change components | Pipeline transitions to NULL state successfully, all stream resources released, and channel change components cleaned up |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 minutes  

**Priority:** High

**Release Version:** M121